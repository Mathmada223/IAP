import re

class IAPFallbackIntent:

    @staticmethod
    def get_fallback(self, said, fallback_keywords):
        fallback = {
            "status": False,
            "response": None
        }

        print(said, fallback_keywords)

        return fallback