module Jekyll
  class PostAssetFile < StaticFile
    def initialize(site, base, dir, name, dest_dir)
      super(site, base, dir, name)
      @dest_dir = dest_dir
    end

    def destination(dest)
      File.join(dest, @dest_dir, @name)
    end
  end

  class CopyAssetsGenerator < Generator
    safe true
    priority :high

    def generate(site)
      # Find all non-index files in _folder_posts subdirectories
      folder_posts_dir = File.join(site.source, "_folder_posts")
      return unless Dir.exist?(folder_posts_dir)

      Dir.glob(File.join(folder_posts_dir, "**", "*")).each do |file|
        next if File.directory?(file)
        next if File.basename(file) == "index.md"

        relative_path = file.sub("#{site.source}/", "")
        dir_name = File.dirname(relative_path).sub("_folder_posts/", "")
        filename = File.basename(file)

        # Match by directory name, not slug (index.md files have slug "index")
        post = site.collections["folder_posts"].docs.find do |doc|
          File.basename(File.dirname(doc.relative_path)) == dir_name
        end

        if post
          # Copy asset to the post's permalink URL path
          site.static_files << PostAssetFile.new(
            site,
            site.source,
            "_folder_posts/#{dir_name}",
            filename,
            post.url
          )
        end
      end
    end
  end
end
