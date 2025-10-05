module Jekyll
  class CopyAssetsGenerator < Generator
    safe true
    priority :high

    def generate(site)
      # Find all files in _folder_posts subdirectories (except index.md)
      folder_posts_dir = File.join(site.source, "_folder_posts")
      return unless Dir.exist?(folder_posts_dir)

      Dir.glob(File.join(folder_posts_dir, "**", "*")).each do |file|
        next if File.directory?(file)
        next if File.basename(file) == "index.md"
        
        relative_path = file.sub("#{site.source}/", "")
        dir_name = File.dirname(relative_path).sub("_folder_posts/", "")
        filename = File.basename(file)
        
        # Find the corresponding post to get its URL
        post = site.collections["folder_posts"].docs.find do |doc|
          doc.data["slug"] == dir_name
        end
        
        if post
          # Copy the file to the post's output directory
          dest_path = File.join(post.url, filename)
          site.static_files << StaticFile.new(
            site,
            site.source,
            "_folder_posts/#{dir_name}",
            filename
          )
        end
      end
    end
  end
end
