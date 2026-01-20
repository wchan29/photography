import conf
import os
from PIL import Image, ImageDraw, ImageFont


class Photo():
    def __init__(self, path):
        self.path = path
        self.min_path = ''
        self.pil_image = Image.open(self.path).convert('RGB')
        self.witdh, self.height = self.pil_image.size
        self.size = self.pil_image.size

        min_file = self.path.stem + '.min' + self.path.suffix
        self.min_path = self.path.with_name(min_file)
    
    @property
    def is_min(self):
        return self.path.match('*.min.jpg')
    
    @property
    def has_min(self):
        return self.min_path.exists()
    
    def format(self):
        if self.is_min:
            return None
        
        if not self.has_min:
            if conf.SIGN_ORIGINAL:
                signed_image = self.mark_image(self.pil_image, conf.fontsize)
                self.save_image(signed_image, self.path)
            
            # resize
            ratio = float(conf.MIN_WIDTH) / self.size[0]
            new_image_size = tuple([int(x*ratio) for x in self.size])

            if conf.SIGN_THUMBNAIL:
                if not conf.SIGN_ORIGINAL:
                    signed_image = self.mark_image(self.pil_image, conf.fontsize)
                signed_image.thumbnail(new_image_size, Image.Resampling.LANCZOS)
                self.save_image(signed_image, self.min_path)
            else:
                min_image = self.pil_image.copy()
                min_image.thumbnail(new_image_size, Image.Resampling.LANCZOS)
                self.save_image(min_image, self.min_path)

        relative_path = str(self.path.relative_to(conf.DIR_PATH))

        # return basic info
        return {
          "type": 'photo',
          'width': self.size[0],
          'height': self.size[1],
          'path': './' + relative_path,
          'min_path': './' + str(self.min_path.relative_to(conf.DIR_PATH))
        }
    
    def save_image(self, img, path):
        if conf.DEBUG:
            img.show()
            return

        rgb = img.convert("RGB")  # ensure no alpha channel
        rgb.save(
            path,
            "JPEG",
            quality=getattr(conf, "JPEG_QUALITY", 92),
            optimize=True,
            progressive=True
        )

    def mark_image(self, img, fontsize):
        img = img.copy()
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('./assets/font/' + conf.fontfamily, fontsize)

        bbox = draw.textbbox((0, 0), conf.copyright, font=font)
        t_w = bbox[2] - bbox[0]
        t_h = bbox[3] - bbox[1]

        width, height = img.size
        x = (width - t_w) / 2
        y = height - 2 * t_h

        # JPEG has no alpha channel, so simulate transparency by using a light gray
        # You can tune this (higher = brighter watermark)
        fill = (235, 235, 235)

        draw.text((x, y), conf.copyright, font=font, fill=fill)
        return img