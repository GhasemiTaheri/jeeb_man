from rest_access_policy import AccessPolicy


class CategoryAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["update", "destroy"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": "is_owner"
        },
        {
            "action": ["list", "create", "retrieve"],
            "principal": ["authenticated"],
            "effect": "allow"
        }
    ]

    def is_owner(self, request, view, action) -> bool:
        # This method is used to protect public categories
        category = view.get_object()
        return category.owner is not None and request.user == category.owner
