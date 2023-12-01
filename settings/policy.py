from rest_access_policy import AccessPolicy


class CategoryAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["*"],
            "principal": ["authenticated"],
            "effect": "allow"
        },
        {
            "action": ["update", "destroy"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": "is_owner"
        }
    ]

    def is_owner(self, request, view, action) -> bool:
        # This method is used to protect public categories
        category = view.get_object()
        return request.user == category.owner
