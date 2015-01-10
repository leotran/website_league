# -*- coding: utf-8 -*-
##############################################################################
#
#    @package league Leagues Management for Odoo 8.0
#    @copyright Copyright (C) 2015 Leo Tran (leotran.hpvn@gmail.com). All rights reserved.#
#    @license http://www.gnu.org/licenses GNU Affero General Public License version 3 or later; see LICENSE.txt
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.addons.web import http
from openerp.addons.web.http import request

class Table(http.Controller):
    
    @http.route(['/table/',
        '/table/season/<model("season"):season>/',
        '/table/competition/<model("league"):league>/',
        '/table/competition/<model("league"):league>/season/<model("season"):season>/',
    ], type='http', auth='public', website=True)
    def table(self, season=None, league=None):
        season_obj = http.request.env['season']
        league_obj = http.request.env['league']
        league_season_obj = http.request.env['league.season']
        
        pl_id = 1
        liga_id = 2
        if league and league.id != 1:
            pl_id = 0
        if league and league.id != 2:
            liga_id = 0
            
        pl_domain = [('league_id','=',pl_id)]
        liga_domain = [('league_id','=',liga_id)]
        if season:
            pl_domain += [('season_id','=',season.id)]
            liga_domain += [('season_id','=',season.id)]
        else:
            pl_domain += [('state','=','open')]
            liga_domain += [('state','=','open')]                
        
        pl_season = league_season_obj.search(pl_domain)
        liga_season = league_season_obj.search(liga_domain)
        league_seasons = http.request.env['league.season.team']
        
        return request.website.render('website_league.index', {
            'seasons': season_obj.search([]),
            'leagues': league_obj.search([]),
            'premier_league': league_seasons.search([('league_season_id','=',pl_season.id)]),
            'liga': league_seasons.search([('league_season_id','=',liga_season.id)]),
            'season': season,
            'league': league, 
        })