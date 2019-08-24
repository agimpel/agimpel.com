from django import forms
from .models import Category, Tag

import logging
logger = logging.getLogger("django")

class FilterForm(forms.Form):

    category_activity = Category.objects.filter(slug="activity")[0]
    category_region = Category.objects.filter(slug="country")[0]

    region_parents = []
    parents_to_check = [category_region]
    while parents_to_check:
        parent = parents_to_check.pop(0)
        region_parents.append(parent)
        if Category.objects.filter(parent=parent):
            parents_to_check.extend(Category.objects.filter(parent=parent))

    all_activities = Tag.objects.filter(category=category_activity)
    all_regions = []
    for region in region_parents:
        all_regions.extend(Tag.objects.filter(category=region))

    choices_activities = [["all", "all"]]
    for activity in all_activities:
        choices_activities.append([category_activity.slug + '.' + activity.slug, activity.title])

    choices_regions = []
    for region in all_regions:
        hierarchical_slug = region.hierarchical_slug()
        title = region.title if not region.parent else " - "+region.title
        choices_regions.append([hierarchical_slug, title])
    choices_regions.sort()
    choices_regions.insert(0, ["all", "all"])
    logger.info(choices_regions)

    activity = forms.ChoiceField(choices=tuple(choices_activities))
    region = forms.ChoiceField(choices=tuple(choices_regions))