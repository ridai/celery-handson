"""Views endpoint
"""

from django.http import JsonResponse, HttpResponse
from django.views import generic
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import time

# Step1
@method_decorator(csrf_exempt, name='dispatch')
class Base(generic.TemplateView):
    """サンプル画面として静的なhtmlを返すだけのシンプルなパターン
    """

    template_name = "start_task.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx


@method_decorator(csrf_exempt, name='dispatch')
class TaskStep1(generic.View):
    """Baseから呼び出される、タスクの実行ロジックエンドポイント
    Step1: 単純にresponseをX秒待つ
    """

    def post(self, request, *args, **kwargs):
        # レスポンスを10秒待つ
        time.sleep(10)
        return redirect(reverse("base"))
