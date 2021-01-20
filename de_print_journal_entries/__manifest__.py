# -*- coding: utf-8 -*-
#################################################################################
# Author      : 
# Copyright(c): 2019 
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
#################################################################################
{
  "name"                 :  "Imprimir Partidas de Diario",
  "summary"              :  "This module will Add Print Option in Journal Entries",
  "category"             :  "Accounting",
  "version"              :  "1.3",
  "sequence"             :  1,
  "author"               :  "SewingSolution",
  "license"              :  "OPL-1",
  "website"              :  "",
  "description"          :  """
This App will Add Print Option in Journal Entries
""",
  "live_test_url"        :  "",
  "depends"              :  [
                             'account'
                            ],
  "data"                 :  [
                             'views/journal_entries_report.xml',
                            ],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  150,
  "currency"             :  "USD",
  "images"		 :['static/description/banner.jpg'],
}