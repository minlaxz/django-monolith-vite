from django.contrib.sites.models import Site


def run(*args):
    site, created = Site.objects.get_or_create(pk=2)
    if "staging" in args:
        site.domain = "dmv-minlaxz.koyeb.app"
        site.name = "DMV by minlaxz"
        site.save()
    print("Site id: ", site.pk)
    print("Site name: ", site.name)
    print("Site doamin: ", site)
