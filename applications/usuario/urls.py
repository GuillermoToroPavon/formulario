from django.urls import path
from . import views

app_name = "usuario_app"

urlpatterns = [
	path(
		'registrar/',
		views.CreateViewUsuario.as_view(),
		name='añadir_usuario'
	),
	path(
		'',
		views.HomeView.as_view(),
		name='home'
	),
	path(
		'pdf/',
		views.render_pdf_view,
		name='pdf'
	),
	path(
		'pdfFirmado/',
		views.firmarPdf,
		name='pdfFirmado'
	),
]