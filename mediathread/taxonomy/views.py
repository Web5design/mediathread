from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from djangohelpers.lib import allow_http, rendered_with
from mediathread.taxonomy.models import VocabularyForm, Vocabulary


@login_required
@allow_http("GET")
@rendered_with('taxonomy/taxonomy_workspace.html')
def taxonomy_workspace(request):
    if not request.course.is_faculty(request.user):
        return HttpResponseForbidden("forbidden")

    return {
        'vocabularies': Vocabulary.objects.get_for_object(request.course),
        'vocabulary_form': VocabularyForm(),
        'course': request.course,
        'course_type': ContentType.objects.get_for_model(request.course)
    }


@login_required
@allow_http("POST")
@rendered_with('taxonomy/taxonomy_workspace.html')
def vocabulary_create(request):
    if not request.course.is_faculty(request.user):
        return HttpResponseForbidden("forbidden")

    form = VocabularyForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('taxonomy-workspace', args=[]))

    return {
        'vocabulary_form': form,
        'course': request.course,
        'course_type': ContentType.objects.get_for_model(request.course)
    }