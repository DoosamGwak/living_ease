from rest_framework.exceptions import ValidationError

class ImageValidator:

    max_size = 5 * 1024 * 1024 
    valid_mime_types = ['image/jpeg', 'image/png']

    def validate_image_size(cls, image):
        if image.size > cls.max_size:
            raise ValidationError(f"이미지 파일 크기가 너무 큽니다. 최대 허용 크기는 {cls.max_size // (1024 * 1024)}MB 입니다.")

    def validate_image_format(cls, image):
        if image.content_type not in cls.valid_mime_types:
            raise ValidationError("지원되지 않는 이미지 형식입니다. JPEG 또는 PNG 파일을 업로드하세요.")
        

class IsAuthorValidator:
    def validate_user_is_author(request_user, board):
        if board.user != request_user:
            raise ValidationError("이 게시글을 수정/삭제할 권한이 없습니다.")