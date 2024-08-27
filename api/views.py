from django.views import generic
from django.http import JsonResponse
from django.contrib.auth.models import User
from jose import jwt
import json
from django.contrib.auth.hashers import make_password
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.core.paginator import Paginator
from rest_framework.generics import ListAPIView
from django.contrib.auth import logout
from allauth.account.models import EmailAddress
import datetime
from django.contrib.auth import login, authenticate
from rest_framework.decorators import api_view
from django.contrib.sites.shortcuts import get_current_site
import logging
from django.core import serializers
from braces.views import CsrfExemptMixin
from django.db.models import F
from rest_framework.views import APIView
from .utils import query_db
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def loadUsr(token):
    user_data = jwt.decode(token, 'Eg{x%^_~&Jxv%D**jZBPvMMXv/brp0', algorithms='HS256')
    usr = User.objects.get(username=user_data["user"])
    return usr


class LoginApiView(CsrfExemptMixin, generic.View):

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body.decode("utf8"))
        user = authenticate(username=body["email"], password=body["password"])
        log_message_api_auth = ''
        exexute_date = datetime.datetime.now()
        if user:
            user_is_activate = EmailAddress.objects.filter(user=user, verified=True)
            if user_is_activate:
                try:
                    user_res = json.loads(serializers.serialize("json", [user, ]))[0]

                    del user_res["fields"]["password"]
                except:
                    pass

                expiry = datetime.date.today() + datetime.timedelta(days=999)
                expiry = str(expiry.day) + "/" + str(expiry.month) + "/" + str(expiry.year)
                token = jwt.encode({'user': user.username, 'expiry': expiry}, 'Eg{x%^_~&Jxv%D**jZBPvMMXv/brp0', algorithm='HS256')
                login(request, user, backend = 'django.contrib.auth.backends.ModelBackend')
                return JsonResponse({"status":200, "token": token})
            else:
                log_message_api_auth = str('Erreur d\'authentification le Compte {} est inactif {}').format(
                    user,
                    exexute_date)
                log = open('bugprog_log.txt', 'a' , encoding='utf-8')
                log.write(log_message_api_auth)
                log.write('\n')
                log.close()
                return JsonResponse({"status": 500, "message":"Votre compte est inactif."})
        else:
            log_message_api_auth = str('Erreur d\'authentification. L\'adresse email {} à essayer de ce connecter avec des identifiants incorrects {}').format(
                    body["email"],
                    exexute_date)
            log = open('bugprog_log.txt', 'a' , encoding='utf-8')
            log.write(log_message_api_auth)
            log.write('\n')
            log.close()
            return JsonResponse({"error": 'Email ou mot de passe incorrects'})


# ###################################################### MODULE GESTION DES LIGNES BUDGETAIRES ########################################
class ligneBudgetaire(CsrfExemptMixin, APIView):

    def get(self, request, *args, **wargs):
        token = request.GET.get('token')
        anneebudgetaire = request.GET.get('anneebudgetaire')
        codestruturemin = request.GET.get('codestruturemin')
        codestruturemax = request.GET.get('codestruturemax')
        log_message_database_connect = ''
        log_message_api_auth = ''
        api_label = str('Webservice Lignes Budgétaire => ')
        exexute_date = datetime.datetime.now()
        try:
            user_data = jwt.decode(token, 'Eg{x%^_~&Jxv%D**jZBPvMMXv/brp0', algorithms='HS256')
        except Exception as e:
            log_message_api_auth = str('{} Echec de l\'Authentification à l\'API le {}.').format(
                api_label, 
                exexute_date)
            log = open('bugprog_log.txt', 'a' , encoding='utf-8')
            log.write(log_message_api_auth)
            log.write('\n')
            log.close()
            return JsonResponse({'status':403, "message": "Votre Token n'est pas valide. Authentifiez vous et reessayez"})
        usr = User.objects.get(username=user_data["user"])
        if usr:
            log_message_api_auth = str('{} Utilisateur {} c\'est connecté avec succès à l\'API le {}').format(
                api_label,
                usr,
                exexute_date)
            results = []
            attr_request = """SELECT 
                        TB.CODESTRUCTURE,
                        TB.LIBELLESTRUCTURE,
                        TL.CODELIGNEBUDGETAIRE,
                        TA.CODETACHE,
                        TA.LIBELLETACHE,
                        TN.CODENATURE,
                        TN.LIBELLENATURE,  
                        TL.EXERCICEBUDGETAIRE, 
                        TL.MONTANTBUDGET, 
                        TL.MONTANTCONSOMMEE, 
                        TL.TRANSFERTPLUS, 
                        TL.TRANSFERTMOINS, 
                        TL.MONTANTSOLLICITE,
                        TL.ORA_ROWSCN
                    FROM 

                        TBLIGNEBUDGETAIRE TL, TBTACHE TA , TBSTRUCTURE TB, TBNATURE TN

                    WHERE

                        TB.ORGANIGRAMME = '2023'

                        AND TL.CODETACHE = TA.CODETACHE

                        AND TB.CODESTRUCTURE = TA.CODESTRUCTURE

                        AND TN.CODENATURE = TL.CODENATURE

                        AND TL.EXERCICEBUDGETAIRE = '{}'

                        AND TL.CODESTRUCTURE IN ('{}','{}')

                        AND LENGTH(TA.CODETACHE) = 7
                    
                    ORDER BY 1""".format(anneebudgetaire, codestruturemin, codestruturemax)
            try:
                query = query_db(attr_request)
            except Exception as e:
                print(e)
                log_message_database_connect = str('{} Erreur de connexion à la base de donnée par l\'utilisateur {} le {}.').format(
                    api_label,
                    usr,
                    exexute_date)
                log = open('bugprog_log.txt', 'a' , encoding='utf-8')
                log.write(log_message_api_auth)
                log.write('\n')
                log.close()
                return JsonResponse({'status':502, "message": "Impossible de se connecter à la Base de donnée"})
            log_message_database_connect = str('{} L\'Utilisateur {} c\'est connecté à la base de donnée avec succès le {}').format(
                api_label,
                usr,
                exexute_date)
            paginator = Paginator(query, 50)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            for i in page_obj:
                results.append(i)
            log = open('bugprog_log.txt', 'a' , encoding='utf-8')
            log.write(log_message_api_auth)
            log.write('\n')
            log.write(log_message_database_connect)
            log.write('\n')
            log.close()
            return JsonResponse({'status':200, 
                'current_page':page_number, 
                'total_page':paginator.num_pages, 
                'results':results, 
                'message': 'Success'},
                safe=False)
        else:
            log = open('bugprog_log.txt', 'a' , encoding='utf-8')
            log.write(log_message_api_auth)
            log.write('\n')
            log.close()
            return JsonResponse({'status':403, "message": "Utilisateur non authentifier"})



# ###################################################### MODULE GESTION DES OPERATIONS ########################################
class OperationBugetaire(CsrfExemptMixin, APIView):

    def get(self, request, *args, **wargs):
        token = request.GET.get('token')
        codestruturemin = request.GET.get('codestruturemin')
        codestruturemax = request.GET.get('codestruturemax')
        datedemandemin = request.GET.get('datedemandemin')
        datedemandemax = request.GET.get('datedemandemax')
        token = request.GET.get('token')
        log_message_database_connect = ''
        log_message_api_auth = ''
        exexute_date = datetime.datetime.now()
        api_label = str('Webservice Opérations Budgétaire => ')
        try:
            user_data = jwt.decode(token, 'Eg{x%^_~&Jxv%D**jZBPvMMXv/brp0', algorithms='HS256')
        except Exception as e:
            log_message_api_auth = str('{} Echec de l\'Authentification à l\'API le {}.').format(
                api_label,
                exexute_date)
            log = open('bugprog_log.txt', 'a' , encoding='utf-8')
            log.write(log_message_api_auth)
            log.write('\n')
            log.close()
            return JsonResponse({'status':403, "message": "Votre Token n'est pas valide. Authentifiez vous et reessayez"})
        usr = User.objects.get(username=user_data["user"])
        if usr:
            log_message_api_auth = str('{} Utilisateur {} c\'est connecté avec succès à l\'API le {}').format(
                api_label,
                usr,
                exexute_date)
            results = []
            attr_request = """
            SELECT 
                TBO.CODEOPERATION, 
                TBO.TYPEDEPENSE, 
                TBO.CODELIGNEBUDGETAIRE, 
                TBO.NUMDEMANDE, 
                TBO.DATEDEMANDE, 
                TBO.PRESTATAIRE, 
                TBO.MOTIF, 
                TBO.ETATOPERATION, 
                TBO.DATECAPRI, 
                TBO.OPERATIONANNULER, 
                TBO.MONTANTOPERATION,
                TBO.CODETYPEDEPENSE, 
                TBO.BC_NUM, 
                TBO.BC_SIGNATURE, 
                TBO.BC_NOTIFICATION, 
                TBO.FACTURE_NUM,
                TBO.ORA_ROWSCN

             FROM 
                TBOPERATION TBO, TBTACHE TA

             WHERE
                SUBSTR(TBO.CODELIGNEBUDGETAIRE, 1, 7) = TA.CODETACHE
                AND TA.CODESTRUCTURE IN ('{}','{}')
                AND TBO.DATEDEMANDE BETWEEN '{}' AND '{}'
              """.format(
                codestruturemin,
                codestruturemax,
                datedemandemin,
                datedemandemax)
            try:
                query = query_db(attr_request)
            except Exception as e:
                print(e)
                log_message_database_connect = str('{} Erreur de connexion à la base de donnée par l\'utilisateur {} le {}.').format(
                    api_label,
                    usr,
                    exexute_date)
                log = open('bugprog_log.txt', 'a' , encoding='utf-8')
                log.write(log_message_api_auth)
                log.write('\n')
                log.close()
                return JsonResponse({'status':502, "message": str("Impossible de se connecter à la Base de donnée. Détail : ")})
            log_message_database_connect = str('{} L\'Utilisateur {} c\'est connecté à la base de donnée avec succès le {}').format(
                api_label,
                usr,
                exexute_date)
            paginator = Paginator(query, 50)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            for i in page_obj:
                results.append(i)
            log = open('bugprog_log.txt', 'a' , encoding='utf-8')
            log.write(log_message_api_auth)
            log.write('\n')
            log.write(log_message_database_connect)
            log.write('\n')
            log.close()
            return JsonResponse({'status':200, 
                'current_page':page_number, 
                'total_page':paginator.num_pages, 
                'results':results, 
                'message': 'Success'},
                safe=False)
        else:
            log = open('bugprog_log.txt', 'a' , encoding='utf-8')
            log.write(log_message_api_auth)
            log.write('\n')
            log.close()
            return JsonResponse({'status':502, "message": "Une erreur cest produite veuillez contacter l'administrateur"})


# ###################################################### MODULE GESTION DES ACTIVITES ########################################
class ActiviteBugetaire(CsrfExemptMixin, APIView):

    def get(self, request, *args, **wargs):
        token = request.GET.get('token')
        codestruturemin = request.GET.get('codestruturemin')
        codestruturemax = request.GET.get('codestruturemax')
        tachemaj = request.GET.get('tachemaj')
        token = request.GET.get('token')
        log_message_database_connect = ''
        log_message_api_auth = ''
        exexute_date = datetime.datetime.now()
        api_label = str('Webservice Tâches Budgétaire => ')
        try:
            user_data = jwt.decode(token, 'Eg{x%^_~&Jxv%D**jZBPvMMXv/brp0', algorithms='HS256')
        except Exception as e:
            log_message_api_auth = str('{} Echec de l\'Authentification à l\'API le {}.').format(
                api_label,
                exexute_date)
            log = open('bugprog_log.txt', 'a' , encoding='utf-8')
            log.write(log_message_api_auth)
            log.write('\n')
            log.close()
            return JsonResponse({'status':403, "message": "Votre Token n'est pas valide. Authentifiez vous et reessayez"})
        usr = User.objects.get(username=user_data["user"])
        if usr:
            log_message_api_auth = str('{} Utilisateur {} c\'est connecté avec succès à l\'API le {}').format(
                api_label,
                usr,
                exexute_date)
            results = []
            attr_request = """
                SELECT 
                    CODEACTIVITE, 
                    CODETACHE, 
                    LIBELLETACHE, 
                    CODESTRUCTURE,
                    TACHEMAJ,
                    ORA_ROWSCN
                FROM 
                    TBTACHE
                WHERE 
                    CODESTRUCTURE IN ('{}','{}') AND TACHEMAJ = '{}'
            """.format(
                codestruturemin,
                codestruturemax,
                tachemaj)
            try:
                query = query_db(attr_request)
            except Exception as e:
                log_message_database_connect = str('{} Erreur de connexion à la base de donnée par l\'utilisateur {} le {}.').format(
                    api_label,
                    usr,
                    exexute_date)
                log = open('bugprog_log.txt', 'a' , encoding='utf-8')
                log.write(log_message_api_auth)
                log.write('\n')
                log.close()
                return JsonResponse({'status':502, "message": "Impossible de se connecter à la Base de donnée"})
            log_message_database_connect = str('{} L\'Utilisateur {} c\'est connecté à la base de donnée avec succès le {}').format(
                api_label,
                usr,
                exexute_date)
            paginator = Paginator(query, 50)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            for i in page_obj:
                results.append(i)
            log = open('bugprog_log.txt', 'a' , encoding='utf-8')
            log.write(log_message_api_auth)
            log.write('\n')
            log.write(log_message_database_connect)
            log.write('\n')
            log.close()
            return JsonResponse({'status':200, 
                'current_page':page_number, 
                'total_page':paginator.num_pages, 
                'results':results, 
                'message': 'Success'},
                safe=False)
        else:
            return JsonResponse({'status':502, "message": "Une erreur cest produite veuillez contacter l'administrateur"})


# ###################################################### MODULE GESTION DES TRANSFERTS ########################################
class TransfertBugetaire(CsrfExemptMixin, APIView):

    def get(self, request, *args, **wargs):
        token = request.GET.get('token')
        codestruturemin = request.GET.get('codestruturemin')
        codestruturemax = request.GET.get('codestruturemax')
        dateoperationmin = request.GET.get('dateoperationmin')
        dateoperationmax = request.GET.get('dateoperationmax')
        token = request.GET.get('token')
        log_message_database_connect = ''
        log_message_api_auth = ''
        exexute_date = datetime.datetime.now()
        api_label = str('Webservice Transferts Budgétaire => ')
        try:
            user_data = jwt.decode(token, 'Eg{x%^_~&Jxv%D**jZBPvMMXv/brp0', algorithms='HS256')
        except Exception as e:
            log_message_api_auth = str('{} Echec de l\'Authentification à l\'API le {}.').format(
                api_label,
                exexute_date)
            log = open('bugprog_log.txt', 'a' , encoding='utf-8')
            log.write(log_message_api_auth)
            log.write('\n')
            log.close()
            return JsonResponse({'status':403, "message": "Votre Token n'est pas valide. Authentifiez vous et reessayez"})
        usr = User.objects.get(username=user_data["user"])
        if usr:
            log_message_api_auth = str('{} Utilisateur {} c\'est connecté avec succès à l\'API le {}').format(
                api_label,
                usr,
                exexute_date)
            results = []
            attr_request = """
            SELECT 
                TB.CODETRANSFERT, 
                TB.SOURCETRANSFERT, 
                TB.DESTINATIONTRANSFERT, 
                TB.DATEOPERATION, 
                TB.MEMO, 
                TB.MONTANTTRANSFERT,
                TB.ORA_ROWSCN

            FROM 
                TBTRANSFERT TB, TBTACHE TA

            WHERE
                SUBSTR(TB.DESTINATIONTRANSFERT, 1, 7) = TA.CODETACHE
                AND TA.CODESTRUCTURE IN ('{}','{}')
                AND TB.DATEOPERATION BETWEEN '{}' AND '{}'
                """.format(
                    codestruturemin,
                    codestruturemax,
                    dateoperationmin,
                    dateoperationmax)
            try:
                query = query_db(attr_request)
            except Exception as e:
                print(e)
                log_message_database_connect = str('{} Erreur de connexion à la base de donnée par l\'utilisateur {} le {}.').format(
                    api_label,
                    usr,
                    exexute_date)
                log = open('bugprog_log.txt', 'a' , encoding='utf-8')
                log.write(log_message_api_auth)
                log.write('\n')
                log.close()
                return JsonResponse({'status':502, "message": "Impossible de se connecter à la Base de donnée"})
            log_message_database_connect = str('{} L\'Utilisateur {} c\'est connecté à la base de donnée avec succès le {}').format(
                api_label,
                usr,
                exexute_date)
            paginator = Paginator(query, 50)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            for i in page_obj:
                results.append(i)
            log = open('bugprog_log.txt', 'a' , encoding='utf-8')
            log.write(log_message_api_auth)
            log.write('\n')
            log.write(log_message_database_connect)
            log.write('\n')
            log.close()
            return JsonResponse({'status':200, 
                'current_page':page_number, 
                'total_page':paginator.num_pages, 
                'results':results, 
                'message': 'Success'},
                safe=False)
        else:
            return JsonResponse({'status':502, "message": "Une erreur cest produite veuillez contacter l'administrateur"})