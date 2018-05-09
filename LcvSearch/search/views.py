import json
from django.shortcuts import render
from django.views.generic.base import View
from search.models import ArticleType
from django.http import HttpResponse
from elasticsearch import Elasticsearch
from datetime import datetime
import redis



client = Elasticsearch(hosts=['127.0.0.1'])
redis_cli = redis.StrictRedis(host='localhost')

# Create your views here.
#首页topn_search
class IndexView(View):
    def get(self,request):
        topn_search = redis_cli.zrevrangebyscore('search_keywords_set', '+inf', '-inf', start=0, num=5)
        return render(request,'index.html',{'topn_search':topn_search,})




class SearchSuggest(View):
    def get(self,request):
        key_word = request.GET.get('s','')
        re_datas = []
        if key_word:
            s = ArticleType.search()
            s = s.suggest('my_suggest',key_word,completion={
                'field':'suggest','fuzzy':{
                    'fuzziness':2,
                },
                'size':10,

            })
            suggestions = s.execute()
            for match in suggestions.suggest.my_suggest[0].options:
                source = match._source
                re_datas.append(source['title'])
            return HttpResponse(json.dumps(re_datas),content_type='application/json')


class SearchView(View):
    def get(self,request):
        key_words = request.GET.get('q','')
        redis_cli.zincrby('search_keywords_set',key_words)
        topn_search = redis_cli.zrevrangebyscore('search_keywords_set','+inf','-inf',start=0,num = 5)
        page = request.GET.get('p','1')
        try:
            page = int(page)
        except:
            page = 1
        jobbole_count = redis_cli.get('jobbole_count')
        start_time = datetime.now()
        response = client.search(
            index = 'jobbole',
            body = {
                "query":{
                    "multi_match":{
                    "query":key_words,
                    "fields":["tags","title","content"]
                    }
                },
            'from':(page-1)*10,
            'size':10,
            "highlight": {
                     "pre_tags": ['<span class="keyWord">'],
                     "post_tags": ["</span>"],
                     "fields":{

                        "title": {},
                        "content": {},

                    }
             }
            }
        )
        end_time = datetime.now()
        last_second = (end_time - start_time).total_seconds()
        total_nums = response['hits']['total']
        if (page%10)>0:
            page_nums = int(total_nums/10)+1
        else:
            page_nums = int(total_nums / 10)

        hit_list = []
        for hit in response["hits"]["hits"]:
            hit_dict = {}
            if "title" in hit["highlight"]:
                hit_dict["title"] =''.join( hit["highlight"]["title"])

            else:
                hit_dict["title"] = hit["_source"]["title"]
            if "content" in hit["highlight"]:
                hit_dict["content"] =''.join( hit["highlight"]["content"])[0:500]

            else:
                hit_dict["content"] = hit["_source"]["content"][0:500]
            hit_dict["create_date"] = hit["_source"]["create_date"]
            hit_dict["url"] = hit["_source"]["url"]

            hit_list.append(hit_dict)
        return render(request,'result.html',{'topn_search':topn_search,'jobbole_count':jobbole_count,'last_second':last_second,'page_nums':page_nums,'total_nums':total_nums,'page':page,"all_hits":hit_list,"key_words":key_words})



