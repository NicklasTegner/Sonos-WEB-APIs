class Households:
    @staticmethod
    def get_households():
        result = utils.make_authenticated_request("/households")
        print(result)
