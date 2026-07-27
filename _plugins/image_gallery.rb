module Jekyll
  class ImageGalleryGenerator < Generator
    safe true
    priority :low

    IMAGE_EXTENSIONS = %w[.png .jpg .jpeg .gif].freeze

    def generate(site)
      images_dir = File.join(site.source, "assets", "images")
      return unless Dir.exist?(images_dir)

      # Folders with their own index.html are standalone pages, not part of
      # the gallery: exclude their images entirely rather than listing them.
      viewer_dirs = Dir.glob(File.join(images_dir, "**", "index.html")).map do |f|
        File.dirname(f).sub("#{images_dir}/", "")
      end.sort

      gallery = Hash.new { |h, k| h[k] = [] }

      Dir.glob(File.join(images_dir, "**", "*")).sort.each do |file|
        next if File.directory?(file)
        next unless IMAGE_EXTENSIONS.include?(File.extname(file).downcase)

        relative = file.sub("#{images_dir}/", "")
        next if viewer_dirs.any? { |vd| relative.start_with?("#{vd}/") }

        folder = File.dirname(relative)
        folder = "" if folder == "."
        gallery[folder] << relative
      end

      site.data["image_gallery"] = gallery
    end
  end
end
