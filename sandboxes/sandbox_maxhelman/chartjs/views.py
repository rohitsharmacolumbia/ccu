# from django.http import JsonResponse 
   
from django.shortcuts import render 
from django.views.generic import View 
from chartjs.models import *
from rest_framework.views import APIView 
from rest_framework.response import Response
import pandas as pd


class HomeView(View): 
    def get(self, request, *args, **kwargs): 
        return render(request, 'chartjs/index.html') 

#view for the homepage
class HomepageView(APIView): 
    authentication_classes = [] 
    permission_classes = []
   
    def get(self, request, format = None):
        '''Gets data from excel spreadsheet and puts into pandas dataframe
        Then, sends to frontend'''
        df = pd.pandas.read_excel('../../data/dataOut/CCU_all_patientData_aggregated.xlsx', index_col=0)
        df_2 = pd.pandas.read_excel('../../data/dataOut/CCU_current_patientData_aggregated.xlsx', index_col=0)
        labels = df['date']
        chartdata_in_ccu = df['in_ccu']
        chartdata_avg_age = df['average_age']
        chartdata_deceased = df['deceased']
        chartdata_indeterminate = df['covid+_(y/n/nt_not_tested)_indeterminate']
        chartdata_negative = df['covid+_(y/n/nt_not_tested)_n']
        chartdata_positive = df['covid+_(y/n/nt_not_tested)_y']
        chartdata_nt = df['covid+_(y/n/nt_not_tested)_nt']
        chartdata_in_ccu_daily = df_2['in_ccu']
        chartdata_avg_age_daily = df_2['average_age']
        #chartdata_deceased_daily = df_2['deceased']
        chartdata_indeterminate_daily = df_2['covid+_(y/n/nt_not_tested)_indeterminate']
        chartdata_negative_daily = df_2['covid+_(y/n/nt_not_tested)_n']
        chartdata_positive_daily = df_2['covid+_(y/n/nt_not_tested)_y']
        chartdata_nt_daily = df_2['covid+_(y/n/nt_not_tested)_nt']

        chartLabel = "People in CCU (Confidential)"
        #send data to view
        data ={ 
                     "labels":labels, 
                     "chartLabel":chartLabel, 
                     "chartdata_in_ccu":chartdata_in_ccu, 
                     "chartdata_avg_age":chartdata_avg_age,
                     "chartdata_deceased":chartdata_deceased,
                     "chartdata_indeterminate":chartdata_indeterminate,
                     "chartdata_negative":chartdata_negative,
                     "chartdata_positive":chartdata_positive,
                     "chartdata_nt": chartdata_nt,
                     "chartdata_in_ccu_daily":chartdata_in_ccu_daily, 
                     "chartdata_avg_age_daily":chartdata_avg_age_daily,
                     "chartdata_indeterminate_daily":chartdata_indeterminate_daily,
                     "chartdata_negative_daily":chartdata_negative_daily,
                     "chartdata_positive_daily":chartdata_positive_daily,
                     "chartdata_nt_daily": chartdata_nt_daily,
                     
             } 
        return Response(data)