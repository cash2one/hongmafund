# -*- coding: utf-8 -*-
"""from ems.models import SeoSites,SiteRank,SiteKeywords,SiteRecord
from lib.siterank import GooglePageRank,AlexaTrafficRank,RankProvider
import time
from django_cron import CronJobBase, Schedule
__author__ = 'cbin'
class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 2 # every 2 hours
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'analyseo.site_alexa_rank'    # a unique code

    def do(self):
        site = SeoSites.objects.filter(siteurl__startswith="http://www.")
        for s in site:
            url = s.siteurl
            alexa = AlexaTrafficRank().get_rank(url)
            if alexa is None:
                alexasum,alexaday = 0,0
            else :
                alexasum,alexaday = alexa[0],alexa[1]
            pr = GooglePageRank().get_rank(url)
            if pr is None:
                pr = 0
            else:
                pr = pr
            print(alexasum,alexaday,pr)
            rank = SiteRank(web_site=SeoSites.objects.get(siteurl=url),alexasum=alexasum,alexaday=alexaday,pr=pr)
            rank.save()
            time.sleep(1)
"""