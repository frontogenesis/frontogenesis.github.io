module Jekyll
  class FolderPostsGenerator < Generator
    safe true
    priority :high

    def generate(site)
      # Find all index.md files in _posts subdirectories
      posts_dir = File.join(site.source, "_posts")
      return unless Dir.exist?(posts_dir)

      Dir.glob(File.join(posts_dir, "**", "index.md")).each do |file|
        relative_path = file.sub("#{site.source}/", "")
        dir_name = File.dirname(relative_path).sub("_posts/", "")
        
        # Read the file content to get front matter
        content = File.read(file)
        
        # Parse front matter manually
        if content =~ /\A(---\s*\n.*?\n?)^(---\s*$\n?)/m
          front_matter = YAML.safe_load($1)
          content = $'
        else
          front_matter = {}
        end
        
        # Create a new document
        doc = Document.new(file, {
          :site => site,
          :collection => site.collections["posts"]
        })
        
        # Set the slug based on the directory name
        doc.data["slug"] = dir_name
        
        # Ensure we have the right data
        doc.data["title"] = front_matter["title"] if front_matter["title"]
        doc.data["date"] = front_matter["date"] if front_matter["date"]
        doc.data["categories"] = front_matter["categories"] if front_matter["categories"]
        doc.data["layout"] = front_matter["layout"] || "post"
        
        # Set the permalink based on date and slug
        if front_matter["date"]
          date = Time.parse(front_matter["date"].to_s)
          doc.data["permalink"] = "/#{date.year}/#{date.month.to_s.rjust(2, '0')}/#{date.day.to_s.rjust(2, '0')}/#{dir_name}/"
        end
        
        # Add to posts collection
        site.collections["posts"].docs << doc
      end
    end
  end
end
