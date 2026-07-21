module Jekyll
  class ImageGalleryGenerator < Generator
    safe true
    priority :low

    IMAGE_EXTENSIONS = %w[.png .jpg .jpeg .gif].freeze

    def generate(site)
      images_dir = File.join(site.source, "assets", "images")
      return unless Dir.exist?(images_dir)

      gallery = Hash.new { |h, k| h[k] = [] }

      Dir.glob(File.join(images_dir, "**", "*")).sort.each do |file|
        next if File.directory?(file)
        next unless IMAGE_EXTENSIONS.include?(File.extname(file).downcase)

        relative = file.sub("#{images_dir}/", "")
        folder = File.dirname(relative)
        folder = "" if folder == "."
        gallery[folder] << relative
      end

      site.data["image_gallery"] = gallery
    end
  end
end
