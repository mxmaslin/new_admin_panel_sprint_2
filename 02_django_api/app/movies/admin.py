# from django.contrib import admin
# from django.utils.translation import gettext_lazy as _
#
# from .models import Filmwork, Person, Genre, PersonFilmwork, GenreFilmwork
#
#
# class PersonInline(admin.TabularInline):
#     model = PersonFilmwork
#     fk_name = 'person'
#     extra = 1
#
#
# class PersonFilmworkInline(admin.TabularInline):
#     model = PersonFilmwork
#     fk_name = 'film_work'
#     extra = 1
#     autocomplete_fields = ('person',)
#
#
# class GenreFilmworkInline(admin.TabularInline):
#     model = GenreFilmwork
#     fk_name = 'film_work'
#     extra = 1
#
#
# class FilmworkAdmin(admin.ModelAdmin):
#     list_display = (
#         'title', 'creation_date', 'rating', 'created', 'modified',
#     )
#     search_fields = ('title', 'creation_date',)
#     list_filter = ('type', 'genres')
#     # inlines = (PersonFilmworkInline, GenreFilmworkInline, )
#     list_prefetch_related = ('genres', 'persons')
#
#
# class PersonAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'created_display', 'modified_display',)
#     search_fields = ('full_name', )
#
#     def created_display(self, obj):
#         return obj.created.strftime("%d %b %Y %H:%M:%S")
#     created_display.short_description = _('Created')
#
#     def modified_display(self, obj):
#         return obj.modified.strftime("%d %b %Y %H:%M:%S")
#     modified_display.short_description = _('Modified')
#
#
# class GenreAdmin(admin.ModelAdmin):
#     list_display = ('name', 'created_display', 'modified_display', )
#
#     def created_display(self, obj):
#         return obj.created.strftime("%d %b %Y %H:%M:%S")
#     created_display.short_description = _('Created')
#
#     def modified_display(self, obj):
#         return obj.modified.strftime("%d %b %Y %H:%M:%S")
#     modified_display.short_description = _('Modified')
#
#
# admin.site.register(Filmwork, FilmworkAdmin)
# admin.site.register(Person, PersonAdmin)
# admin.site.register(Genre, GenreAdmin)
#
#
# class GenreFilmworkAdmin(admin.ModelAdmin):
#     pass
# class PersonFilmworkAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(GenreFilmwork, GenreFilmworkAdmin)
# admin.site.register(PersonFilmwork, PersonFilmworkAdmin)
