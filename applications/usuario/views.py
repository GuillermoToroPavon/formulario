from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, View
from .models import usuario
from django.urls import reverse_lazy
from django.http import HttpResponse, FileResponse
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from xhtml2pdf import pisa
from django.conf import settings
import subprocess
import os
# Create your views here.

#Función que devuelve true si la letra del dni esta correcta, false para incorrecta
#Arreglar (era demasiado larga y pesada)
def validateDNI(dni):
	numbers = dni[0:8]
	letter = dni[8:9]
	validate = int(numbers)%23
	returned = False
	return returned


def signedPDF(request):
	return render(request, "usuario/pdfFirmado.html")


#Función que recoge los datos del usuario registrado y genera el pdf, luego lo envia a una página de html para mostrarlo
def render_pdf_view(request):
	formulario = usuario.objects.last()
	template_path = 'usuario/plantillaPDF.html'
	context = {'formulario': formulario}#el objeto que tiene los datos

	filename = formulario.name + formulario.firstSurname + formulario.secondSurname + str(formulario.id) +'.pdf'
	filepath = os.path.join(settings.MEDIA_ROOT, filename)
	file = open(filepath, 'wb')

	template = get_template(template_path)
	html = template.render(context)
	pisa_status = pisa.CreatePDF(html, dest=file)

	file.close()

	if pisa_status.err:
		return HttpResponse('Han habido algunos problemas <pre>' + html + '</pre>')
	
	readFile = open(filepath, 'rb')
	
	response = FileResponse(readFile)
	response['Content-Type'] = 'application/pdf'
	response['Content-Disposition'] = 'inline; filename="myfile.pdf"'
	
	showPath = os.path.join('/media/', filename)
	context = {'pdf': response}
	diccionario = {'showPath' : showPath}
	return render(request, "usuario/pdf.html", diccionario)


#Función que firma un pdf con la firma digital y luego lo envia a una página html para mostrarlo
def firmarPdf(request):
	pdfAFirmar = usuario.objects.last()
	filename = pdfAFirmar.name + pdfAFirmar.firstSurname + pdfAFirmar.secondSurname + str(pdfAFirmar.id) +'.pdf'
	filepath = os.path.join(settings.MEDIA_ROOT, filename)
	secondaryFilename = pdfAFirmar.name + pdfAFirmar.firstSurname + pdfAFirmar.secondSurname + str(pdfAFirmar.id) + '_signed' + '.pdf'
	secondaryFilepath = os.path.join(settings.MEDIA_ROOT, secondaryFilename)
	p = subprocess.run(['autofirma', 'sign', '-i', filepath, '-certgui', '-o', secondaryFilepath, '-format', 'auto'])

	readFile = open(secondaryFilepath, 'rb')

	response = FileResponse(readFile)
	response['Content-Type'] = 'application/pdf'
	response['Content-Disposition'] = 'inline; filename="myfile.pdf"'

	showPath = os.path.join('/media/', secondaryFilename)
	context = {'pdf': response}
	diccionario = {'showPath' : showPath}

	return render(request, "usuario/pdfFirmado.html", diccionario)


class CreateViewUsuario(CreateView):
	template_name = 'usuario/registrar.html'
	model = usuario
	context_object_name = 'lista'
	fields = [
		'dni',
		'name',
		'firstSurname',
		'secondSurname',
		'text',
	]
	stringDNI = "31019919A"
	validateDNI(stringDNI)
	success_url = reverse_lazy('usuario_app:pdf')


class HomeView(TemplateView):
	template_name = 'home.html'
	

class PdfView(TemplateView):
	template_name = 'usuario/pdf.html'