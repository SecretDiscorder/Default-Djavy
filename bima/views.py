from django.shortcuts import render
from decimal import Decimal, getcontext
import roman
import io
from io import StringIO
import decimal
from django.http import JsonResponse, HttpResponse
import json
from .shell import run  # Import your custom language interpreter function
from bs4 import BeautifulSoup
import math
getcontext().prec = decimal.MAX_PREC

from .text_morse import morse_translate, reverse_morse_translate
from django.views.decorators.csrf import csrf_exempt
from .jvdict import Jvdict
from .transliteratejav import transliterate
from .aksara import dotransliterate
from django.conf import settings
from django.views.generic import View
import os
class StaticFilesView(View):
    def get(self, request, filename):
        static_dir = settings.BASE_DIR / 'bima/static/'
        file_path = os.path.join(static_dir, filename)
        
        # Check if the requested file exists
        if os.path.exists(file_path) and os.path.isfile(file_path):
            # Open the file in binary mode
            with open(file_path, 'rb') as f:
                # Read the file content
                file_content = f.read()
            
            # Determine the content type based on the file extension
            content_type = 'application/octet-stream'
            if filename.endswith('.png'):
                content_type = 'image/png'
            elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
                content_type = 'image/jpeg'
            elif filename.endswith('.svg'):
                content_type = 'image/svg'
            elif filename.endswith('.css'):
                content_type = 'text/css'
            elif filename.endswith('.js'):
                content_type = 'text/javascript'
            # Return the file content with appropriate content type
            return HttpResponse(file_content, content_type=content_type)
        
        # If the file is not found, return a 404 response
        return HttpResponse(status=404)

            
def index(request):
    return render(request, 'index.html')
def aksara_converter(request):
    if request.method == 'POST':
        text_to_convert = request.POST.get('text_to_convert', '')
        converted_text = dotransliterate(text_to_convert)
        image = generate_image(converted_text)

        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode()


        return render(request, 'aksara/convert.html', {'image': image_base64, 'converted_text': converted_text})

    return render(request, 'aksara/convert.html')
def morse(request):
    result = ""
    expression = request.POST.get('expression', '')
    if 'morse' in request.POST:
        result = morse_translate(expression)
    elif 'latin' in request.POST:
        result = reverse_morse_translate(expression)

    return render(request, 'morse.html', {'result' : result})
def convert_image(request):

    if request.method == 'POST':

        try:
            
            dicts = Jvdict()
            # Ambil gambar dari formulir

            aksara_text = request.POST.get('aksara_text', '')
            translated_text = ' '.join(transliterate(aksara_text, dicts.return_javtolatin()))
            # Path untuk menyimpan gambar sementara
            image = generate_image(translated_text)
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode()


            # Menampilkan hasil pada template
            return render(request, 'aksara/convert_image.html', {'image': image_base64, 'translated_text': translated_text})

        except Exception as e:
            # Tangani kesalahan
            return render(request, 'aksara/error.html', {'error_message': str(e)})
            
    return render(request, 'aksara/convert_image.html')

# Create your views here.
def calculate_result(expression):
    
    try:
        
        expression = expression
        result = Decimal(eval(expression))
        return str(result)
    except Exception as e:
        return "Error"
@csrf_exempt
def kalkulator(request):
    result = ""

    if request.method == 'POST':
        expression = request.POST.get('expression', '')
        result = calculate_result(expression)
        if 'log' in request.POST :
            try:
                angka = expression.split()
                a = int(angka[0])
                b = int(angka[1])
                if b == '':
                    
                    result = math.log(a)
                elif b == '10':
                    result = math.log10(a)
                else :
                    result = math.log(a, b)
            except Exception as e:
                result = "Gunakan 2 angka dipisah spasi"
        if 'to_roman' in request.POST:
            try:
                result = roman.toRoman(int(expression))
            except ValueError or IndexError:
                result = "Invalid number must be 0 - 4999"
            except Exception:
                result = "Invalid number must be 0 - 4999"
        elif 'from_roman' in request.POST:
            roman_number = expression
            try:
                result = roman.fromRoman(roman_number)
            except roman.InvalidRomanNumeralError:
                result = "Invalid Roman numeral"
        elif 'sin' in request.POST:
            sin = expression
            try:
                result = math.sin(float(sin))
            except ValueError:
                result = "error"
        elif 'cos' in request.POST:
            cos = expression
            try:
                result = math.cos(float(cos))
            except ValueError:
                result = "error"
        elif 'tan' in request.POST:
            tan = expression
            try:
                result = math.tan(float(tan))
            except ValueError:
                result = "error"
        elif 'asin' in request.POST:
            asin = expression
            try:
                result = math.asin(float(asin))
            except ValueError:
                result = "error"
        elif 'acos' in request.POST:
            acos = expression
            try:
                result = math.acos(float(acos))
            except ValueError:
                result = "error"
        elif 'atan' in request.POST:
            atan = expression
            try:
                result = math.atan(float(atan))
            except ValueError:
                result = "error"
        elif 'factorial' in request.POST:
            fact = expression
            try:
                result = math.factorial(int(fact))
            except ValueError:
                result = "Dont use comma"
        elif 'c_to_f' in request.POST:
            celcius = float(expression)
            try:
                result = ((celcius * 9/5) + 32)
            except ValueError:
                result = "error"
        elif 'f_to_c' in request.POST:
            fahrenheit = float(expression)
            try:
                result = ((fahrenheit - 32) * 5/9)
            except ValueError:
                result = "error"
        elif 'c_to_k' in request.POST:
            celcius = expression
            try:
                result = (float(celcius) + 273.15)
            except ValueError:
                result = "error"
        elif 'k_to_c' in request.POST:
            kelvin = float(expression)
            try:
                result = (kelvin - 273.15)
            except ValueError:
                result = "error"
        elif 'c_to_r' in request.POST:
            celcius = float(expression)
            try:
                result = (celcius * 4/5)
            except ValueError:
                result = "error"
        elif 'r_to_c' in request.POST:
            reamur = float(expression)
            try:
                result = (reamur * 5/4)
            except ValueError:
                result = "error"
        elif 'r_to_c' in request.POST:
            reamur = float(expression)
            try:
                result = (float(reamur) * 5/4)
            except ValueError:
                result = "error"
        elif 'f_to_r' in request.POST:
            fahrenheit = float(expression)
            try:
                result = ((fahrenheit - 32) * 4/9)
            except ValueError:
                result = "error"
        elif 'f_to_k' in request.POST:
            fahrenheit = float(expression)
            try:
                result = ((fahrenheit + 459.67)* 5/9)
            except ValueError:
                result = "error"
        elif 'r_to_f' in request.POST:
            reamur = float(expression)
            try:
                result = ((reamur * 9/4) + 32)
            except ValueError:
                result = "error"
        elif 'r_to_k' in request.POST:
            reamur = float(expression)
            try:
                result = ((reamur * 5/4) + 273.15)
            except ValueError:
                result = "error"
        elif 'k_to_r' in request.POST:
            kelvin = float(expression)
            try:
                result = ((kelvin - 273.15) * 4/5)
            except ValueError:
                result = "error"
        elif 'k_to_f' in request.POST:
            kelvin = float(expression)
            try:
                result = ((kelvin * 9/5) - 459.67)
            except ValueError:
                result = "error"
        elif 'binary' in request.POST:
            n = int(expression)
            try:
                result = format(n ,"b")
            except ValueError:
                result = "Don't use comma"
        elif 'num' in request.POST:
            n = expression
            try:
                result = int(n, 2)
            except ValueError:
                result = "Not Binary"
                
        elif 'sqrt' in request.POST:
            n = int(expression)
            try:
                result = math.sqrt(n)
            except ValueError:
                result = "Invalid Number"

            
    return render(request, 'kalkulator.html', {'result': result})
    
def blang(request):
    try:
        output_result = ""
        selisih = 0.0
        output = ""
        if request.method == 'POST':
            input_code = request.POST.get('input_code', '')
            html_string = input_code
            soup = BeautifulSoup(html_string, 'html.parser')
            text = soup.get_text()

            if text.strip() != "":
                old_stdout = sys.stdout
                new_stdout = StringIO()
                sys.stdout = new_stdout

                # Execute the custom language interpreter function
                result, error = run('<stdin>', text)

                # Restore stdout to its original value
                sys.stdout = old_stdout

                # Get the output from StringIO
                output = new_stdout.getvalue()
                
                # Check if result is a list=
                if error:
                    output_result = repr(error.as_string())  # Ubah error menjadi string
                elif result:
                    if hasattr(result, 'elements') and len(result.elements) == 1:
                        output_result = repr(result.elements[0])
                        output = output_result
                    else:
                        # Check if result is a list
                        if isinstance(result, list):
                            output_result = json.dumps(result)  # Convert list to JSON string

                        else:
                            output_result = repr(result)

    except Exception as e:
        # Handle specific exceptions if needed
        print(f"An error occurred: {e}")
        output_result = f"An error occurred: {e}"

    return render(request, 'bkang.html', {'output_result': output_result, 'output': output})

