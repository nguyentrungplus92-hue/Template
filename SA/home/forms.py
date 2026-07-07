"""
Form mẫu đủ các loại trường - dùng làm template cho form Thêm/Sửa.

Django Forms tự lo:
- Sinh HTML input đúng loại (date -> lịch, number -> ô số...).
- Validate: trường bắt buộc, đúng kiểu (ngày/số), độ dài, giá trị hợp lệ.
- Báo lỗi từng trường nếu nhập sai.

Khi dùng thật: đổi các trường dưới đây cho khớp dữ liệu của bạn.
Nếu gắn với model (bảng database), cân nhắc dùng forms.ModelForm để tự
sinh trường từ model - gọn hơn (xem chú thích cuối file).
"""
from django import forms


# Lựa chọn mẫu cho các trường select/checkbox
VENDOR_CHOICES = [
    ('', '-- Chọn Vendor --'),
    ('A', 'Vendor A'),
    ('B', 'Vendor B'),
    ('C', 'Vendor C'),
]

STATUS_CHOICES = [
    ('ok', 'Hoạt động'),
    ('warn', 'Cảnh báo'),
    ('danger', 'Tạm dừng'),
]

TAG_CHOICES = [
    ('fico', 'FICO'),
    ('mm', 'MM'),
    ('sd', 'SD'),
]


class RouteForm(forms.Form):
    """Form mẫu - minh họa mọi loại trường thường dùng."""

    # --- CHỮ NGẮN (text) ---
    code = forms.CharField(
        label='Mã Route',
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'VD: RT001'}),
    )
    name = forms.CharField(
        label='Tên tuyến',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'VD: Hà Nội - Hải Phòng'}),
    )

    # --- SỐ (number) ---
    days = forms.IntegerField(
        label='Số ngày đi đường',
        min_value=0, max_value=365,
        widget=forms.NumberInput(attrs={'placeholder': '0'}),
    )
    price = forms.DecimalField(
        label='Đơn giá (VNĐ)',
        required=False, min_value=0, max_digits=12, decimal_places=0,
        widget=forms.NumberInput(attrs={'placeholder': '0'}),
    )

    # --- NGÀY (date) ---
    start_date = forms.DateField(
        label='Ngày bắt đầu',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    # --- NGÀY GIỜ (datetime) ---
    updated_at = forms.DateTimeField(
        label='Thời điểm cập nhật',
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    )

    # --- LỰA CHỌN MỘT (dropdown) ---
    vendor = forms.ChoiceField(
        label='Vendor',
        choices=VENDOR_CHOICES,
    )
    status = forms.ChoiceField(
        label='Trạng thái',
        choices=STATUS_CHOICES,
        widget=forms.RadioSelect,     # hiện dạng nút radio thay vì dropdown
        initial='ok',
    )

    # --- LỰA CHỌN NHIỀU (checkbox nhiều) ---
    tags = forms.MultipleChoiceField(
        label='Nhãn',
        choices=TAG_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    # --- BẬT/TẮT (checkbox đơn) ---
    is_active = forms.BooleanField(
        label='Đang kích hoạt',
        required=False,
        initial=True,
    )

    # --- CHỮ DÀI (textarea) ---
    note = forms.CharField(
        label='Ghi chú',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ghi chú thêm...'}),
    )

    # --- VALIDATE TÙY CHỈNH (ví dụ) ---
    def clean_code(self):
        """Ví dụ kiểm tra riêng: mã phải bắt đầu bằng 'RT'."""
        code = self.cleaned_data['code'].strip().upper()
        if not code.startswith('RT'):
            raise forms.ValidationError('Mã Route phải bắt đầu bằng "RT".')
        return code


# ============================================================
# GHI CHÚ: nếu form gắn với MODEL (bảng database), dùng ModelForm
# sẽ gọn hơn - Django tự sinh trường từ model:
#
#   class RouteForm(forms.ModelForm):
#       class Meta:
#           model = Route
#           fields = ['code', 'name', 'days', 'vendor', 'status', ...]
#           widgets = {
#               'start_date': forms.DateInput(attrs={'type': 'date'}),
#           }
#
# Khi đó view có thể form.save() để lưu thẳng vào database.
# ============================================================
