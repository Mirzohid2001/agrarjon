from .serializers import *
from django.db.models import Sum
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import pandas as pd
import io
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows

from users.models import User


# Create your views here.

class UserCountAPIView(APIView):
    def get(self, request, format=None):
        total_users = User.objects.count()
        if request.user.is_authenticated:
            try:
                statistic = Statistic.objects.get(user=request.user)
            except Statistic.DoesNotExist:
                statistic = Statistic(user=request.user, count=1)
                statistic.save()
            else:
                statistic.count += 1
                statistic.save()
        registered_users_count = Statistic.objects.aggregate(total_registered_users=Sum('count'))[
            'total_registered_users']

        return Response({
            'total_users': total_users
        })


class LegalDocuments(APIView):
    def get(self, request, format=None):
        legal_documents = Legal_Documents.objects.all()
        serializer = Legal_DocumentsSerializer(legal_documents, many=True)
        return Response(serializer.data)


class NewsList(APIView):
    def get(self, request, format=None):
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)


class NewsDetail(APIView):
    def get(self, request, pk, format=None):
        news = News.objects.get(pk=pk)
        serializer = NewsSerializer(news)
        return Response(serializer.data)


class BannerList(APIView):
    def get(self, request, format=None):
        banners = Banner.objects.all()
        serializer = BannerSerializer(banners, many=True)
        return Response(serializer.data)


class CalculateCostAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            region = request.query_params.get('region')
            seed_name = request.query_params.get('seed')
            areas_to_sow = request.query_params.get('areas_to_sow')

            if not region or not seed_name or not areas_to_sow:
                return Response({'error': 'Регион, имя семени и площадь для посева обязательны.'},
                                status=status.HTTP_400_BAD_REQUEST)

            areas_to_sow = int(areas_to_sow)
            try:
                area = Area.objects.get(name=region)
            except Area.DoesNotExist:
                return Response({'error': 'Регион не существует'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                seed = Seed.objects.get(name=seed_name, area=area)
            except Seed.DoesNotExist:
                return Response({'error': 'Семя не существует в указанном регионе'},
                                status=status.HTTP_400_BAD_REQUEST)

            seed_cost = seed.price * areas_to_sow if seed.price else 0

            response_data = {
                'region': region,
                'seed': seed_name,
                'areas_to_sow': areas_to_sow,
                'seed_cost': seed_cost
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            region = request.data.get('region')
            seed_name = request.data.get('seed')
            areas_to_sow = request.data.get('areas_to_sow')
            user_id = request.data.get('user_id')

            if not region or not seed_name or not areas_to_sow or not user_id:
                return Response({'error': 'Регион, имя семени, площадь для посева и ID пользователя обязательны.'},
                                status=status.HTTP_400_BAD_REQUEST)

            areas_to_sow = int(areas_to_sow)
            try:
                area = Area.objects.get(name=region)
            except Area.DoesNotExist:
                return Response({'error': 'Регион не существует'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                seed = Seed.objects.get(name=seed_name, area=area)
            except Seed.DoesNotExist:
                return Response({'error': 'Семя не существует в указанном регионе'},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': 'Пользователь не существует'}, status=status.HTTP_400_BAD_REQUEST)

            workers = Worker.objects.filter(area=area, seed=seed)
            tractors = Tractor.objects.filter(area=area, seed=seed)
            fertilisers = Fertiliser.objects.filter(area=area, seed=seed)
            work_types = WorkType.objects.filter(traktor__area=area, seed=seed)
            seed_cost = seed.price * areas_to_sow if seed.price else 0

            worker_cost_details = [
                {'hours': worker.hour, 'unit_price': worker.salary, 'total': worker.salary * worker.hour} for worker in
                workers if worker.salary and worker.hour]
            worker_cost = sum(item['total'] for item in worker_cost_details)

            tractor_cost_details = [
                {'hours': tractor.hour, 'unit_price': tractor.price, 'total': tractor.price * tractor.hour} for tractor
                in tractors if tractor.price and tractor.hour]
            tractor_cost = sum(item['total'] for item in tractor_cost_details)

            fertiliser_cost_details = [{'unit_price': fertiliser.price, 'total': fertiliser.price} for fertiliser in
                                       fertilisers if fertiliser.price]
            fertiliser_cost = sum(item['total'] for item in fertiliser_cost_details)

            work_type_cost_details = [{'work_hours': work_type.traktor.hour, 'unit_price': work_type.traktor.price,
                                       'total': work_type.traktor.price * work_type.traktor.hour} for work_type in
                                      work_types if work_type.traktor.price and work_type.traktor.hour]
            work_type_cost = sum(item['total'] for item in work_type_cost_details)

            total_cost = seed_cost + worker_cost + tractor_cost + fertiliser_cost + work_type_cost
            cost_per_hectare = total_cost / areas_to_sow if areas_to_sow else 0

            summary_data = {
                'Категория': ['Семена', 'Рабочие', 'Тракторы', 'Удобрения', 'Типы работ', 'Итого'],
                'За единицу': [seed.price, '', '', '', '', ''],
                'Стоимость за гектар': [seed.price, worker_cost / areas_to_sow, tractor_cost / areas_to_sow,
                                        fertiliser_cost / areas_to_sow, work_type_cost / areas_to_sow,
                                        cost_per_hectare],
                'Общая стоимость': [seed_cost, worker_cost, tractor_cost, fertiliser_cost, work_type_cost, total_cost]
            }
            summary_df = pd.DataFrame(summary_data)

            worker_df = pd.DataFrame(worker_cost_details)
            worker_df.insert(0, 'Категория', 'Рабочие')
            worker_df.insert(3, 'За единицу', worker_df['unit_price'])
            worker_df.rename(columns={'unit_price': 'Стоимость'}, inplace=True)

            tractor_df = pd.DataFrame(tractor_cost_details)
            tractor_df.insert(0, 'Категория', 'Тракторы')
            tractor_df.insert(3, 'За единицу', tractor_df['unit_price'])
            tractor_df.rename(columns={'unit_price': 'Стоимость'}, inplace=True)

            fertiliser_df = pd.DataFrame(fertiliser_cost_details)
            fertiliser_df.insert(0, 'Категория', 'Удобрения')
            fertiliser_df.insert(2, 'За единицу', fertiliser_df['unit_price'])
            fertiliser_df.rename(columns={'unit_price': 'Стоимость'}, inplace=True)

            work_type_df = pd.DataFrame(work_type_cost_details)
            work_type_df.insert(0, 'Категория', 'Типы работ')
            work_type_df.insert(3, 'За единицу', work_type_df['unit_price'])
            work_type_df.rename(columns={'unit_price': 'Стоимость'}, inplace=True)

            excel_file = io.BytesIO()
            wb = Workbook()

            summary_ws = wb.active
            summary_ws.title = "Сводка"

            for r_idx, row in enumerate(dataframe_to_rows(summary_df, index=False, header=True), 1):
                for c_idx, value in enumerate(row, 1):
                    cell = summary_ws.cell(row=r_idx, column=c_idx, value=value)
                    cell.border = Border(left=Side(style='thin'), right=Side(style='thin'),
                                         top=Side(style='thin'), bottom=Side(style='thin'))
                    if r_idx == 1:
                        cell.fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
                        cell.font = Font(bold=True, color="FFFFFF")
                        cell.alignment = Alignment(horizontal="center", vertical="center")
                    else:
                        cell.alignment = Alignment(horizontal="center", vertical="center")

            for column in summary_ws.columns:
                max_length = 0
                column = list(column)
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                summary_ws.column_dimensions[column[0].column_letter].width = adjusted_width

            def create_sheet_with_data(wb, title, df):
                ws = wb.create_sheet(title=title)
                for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
                    for c_idx, value in enumerate(row, 1):
                        cell = ws.cell(row=r_idx, column=c_idx, value=value)
                        cell.border = Border(left=Side(style='thin'), right=Side(style='thin'),
                                             top=Side(style='thin'), bottom=Side(style='thin'))
                        if r_idx == 1:
                            cell.fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
                            cell.font = Font(bold=True, color="FFFFFF")
                            cell.alignment = Alignment(horizontal="center", vertical="center")
                        else:
                            cell.alignment = Alignment(horizontal="center", vertical="center")

                for column in ws.columns:
                    max_length = 0
                    column = list(column)
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = (max_length + 2)
                    ws.column_dimensions[column[0].column_letter].width = adjusted_width

            create_sheet_with_data(wb, "Рабочие", worker_df)
            create_sheet_with_data(wb, "Тракторы", tractor_df)
            create_sheet_with_data(wb, "Удобрения", fertiliser_df)
            create_sheet_with_data(wb, "Типы работ", work_type_df)

            wb.save(excel_file)
            excel_file.seek(0)
            file_name = 'cost_estimation.xlsx'
            path = default_storage.save(f'excel_files/{file_name}', ContentFile(excel_file.getvalue()))

            order = Order.objects.create(
                user=user,
                excel_file=path
            )

            return Response({'file_path': path, 'order_id': order.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
