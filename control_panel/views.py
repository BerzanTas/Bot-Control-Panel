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
    global bot_process

    try:
        if request.session.get('bot_running', False) and bot_process is not None:
            # Stop the bot if it is urnning
            bot_process.terminate()
            bot_process = None
            request.session['bot_running'] = False
            return JsonResponse({'status': 'stopped'})
        else:
            # Run the bot
            print("Running the pokebot...")

            bot_process = subprocess.run(
                ['python3', '/home/ubuntu/django/selenium/pokebot.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Read the output
            stdout, stderr = bot_process.communicate()

            if stdout:
                print(f"Bot output: {stdout.decode('utf-8')}")
            if stderr:
                print(f"Bot error: {stderr.decode('utf-8')}")

            request.session['bot_running'] = True
            return JsonResponse({'status': 'started'})
    except Exception as e:
        print("Error while running the pokebot:", e)
        print(traceback.format_exc())
        return JsonResponse({'status': 'error', 'message': str(e)})
