from .forms import CouponSearchForm


def coupon_search_form(request):
    return {"coupon_search_form": CouponSearchForm()}
