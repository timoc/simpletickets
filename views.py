# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from models import Ticket
from forms import TicketForm, TicketFormAdmin
from settings import BASE_TEMPLATE


# MIXINS
class ContextMixin(SuccessMessageMixin, View):
    def get_context_data(self, **kwargs):
        context = super(ContextMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['base_template'] = BASE_TEMPLATE
        return context


class Login_required_mixin(View):
    @classmethod
    def as_view(self, **kwargs):
        return login_required(
                super(Login_required_mixin, self).as_view(**kwargs)
                )


class TicketMixin(object):
    def get_queryset(self):
        if self.request.user.is_staff:
            return Ticket.objects.filter(user__is_staff=False)
        return Ticket.objects.filter(user=self.request.user)

    def get_object(self):
        return self.get_queryset().get(id=self.kwargs['ticket_id'])
# END MIXINS


class TicketCreate(ContextMixin, Login_required_mixin, CreateView):
    title = _('Edit ticket')
    model = Ticket
    fields = ['ticket_type', 'severity', 'description', 'attachment', ]
    success_message = _('ticket was successfully created')
    error_message = _('Please check the failures bellow')
    success_url = reverse_lazy('ticketList')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TicketCreate, self).form_valid(form)


class TicketCreateResponse(ContextMixin, Login_required_mixin, CreateView):
    title = _('Edit ticket')
    model = Ticket
    fields = ['ticket_type', 'severity', 'state', 'resolution_text', ]
    success_message = _('response was successfully created')
    error_message = _('Please check the failures bellow')
    success_url = reverse_lazy('ticketList')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.ticket = Ticket.objects.get(
                id=self.kwargs.get('ticket_id'))
        return super(TicketCreateResponse, self).form_valid(form)


class TicketUpdate(ContextMixin, Login_required_mixin, TicketMixin,
        UpdateView):
    title = _('Edit ticket')
    model = Ticket
    fields = ['ticket_type', 'severity', 'description', 'attachment', ]
    success_message = _('ticket was successfully updated')
    error_message = _('Please check the failures bellow')
    success_url = reverse_lazy('ticketList')

    def get_form_class(self):
        if self.request.user.is_staff:
            return TicketFormAdmin
        return TicketForm


class TicketDelete(ContextMixin, Login_required_mixin, TicketMixin,
        DeleteView):
    title = _('Delete ticket')
    model = Ticket
    success_url = reverse_lazy('home')
    success_message = _('ticket was successfully deleted')
    success_url = reverse_lazy('ticketList')


class TicketList(ContextMixin, Login_required_mixin, TicketMixin, ListView):
    model = Ticket
    title = _('Ticket list')
