# main_app/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import subprocess
from django.http import JsonResponse

selenium_process = None

@login_required
def home(request):
    return render(request, 'control_panel/home.html')

@login_required
def run_pokebot(request):
    global selenium_process
    if request.method == 'POST':
        # Running selenium in seperate process
        if selenium_process is None:
            try:
                python_path = '/home/ubuntu/django/env/bin/python3'
                selenium_process = subprocess.Popen([python_path, '/home/ubuntu/poke_bot.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, errors = selenium_process.communicate()

                if selenium_process.returncode == 0:
                    return JsonResponse({'status': 'PokeBot started', 'output': output.decode()})
                else:
                    return JsonResponse({'status': 'Error executing script', 'errors': errors.decode()})
            except Exception as e:
                return JsonResponse({'status': 'Failed to run script', 'error': str(e)})
        else:
            return JsonResponse({'status': 'PokeBot is already running'})
    return JsonResponse({'status': 'Invalid request'})
