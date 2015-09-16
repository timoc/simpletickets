# -*- coding: utf-8 -*-
from django.conf.urls import include, patterns, url
from django.contrib import admin

from views import TicketList, TicketCreate, TicketDelete, TicketUpdate

from simpletickets.settings.ticketSettings import (TICKET_REST_API,
        API_BASE_URL
    )  # noqa

from api.views import (UserTicketListCreate, UserTicketUpdateDelete,
        StaffTicketList, StaffTicketUpdate
    )

admin.autodiscover()

urlpatterns = patterns('',
        url(r'^$', TicketList.as_view(), name='ticketList'),
        url(r'^new-ticket/$', TicketCreate.as_view(), name='newTicket'),
        url(r'^edit-ticket-(?P<ticket_id>[\d]*)/$',
                TicketUpdate.as_view(), name='TicketUpdate'
            ),
        url(r'^delete-ticket-(?P<ticket_id>[\d]*)/$',
                TicketDelete.as_view(), name='TicketDelete'
            ),
    )

if TICKET_REST_API:
    urlpatterns += patterns('',
            url(r'^{url}/list-create/$'.format(url=API_BASE_URL),
                    UserTicketListCreate.as_view(),
                    name='apiListCreate'
                ),
            url(r'^{url}/ticket-(?P<pk>[\d]+)-update-destroy/$'.format(
                    url=API_BASE_URL
                ),
                    UserTicketUpdateDelete.as_view(),
                    name='updateDestroyCreate'
                ),
            url(r'^{url}/staff-list/$'.format(url=API_BASE_URL),
                    StaffTicketList.as_view(),
                    name='apiListCreate'
                ),
            url(r'^{url}/staff-ticket-(?P<pk>[\d]+)-update/$'.format(
                    url=API_BASE_URL
                ),
                    StaffTicketUpdate.as_view(),
                    name='updateDestroyCreate'
                ),
        )
