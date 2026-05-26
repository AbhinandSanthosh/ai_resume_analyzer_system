from fastapi import Depends, HTTPException

from backend.auth.auth_bearer import verify_token


class RoleChecker:

    def __init__(self, allowed_roles):

        self.allowed_roles = allowed_roles


    def __call__(
        self,
        user=Depends(verify_token)
    ):

        if user["role"] not in self.allowed_roles:

            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )

        return user