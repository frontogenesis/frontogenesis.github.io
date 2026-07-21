---
layout: page
title: Image Gallery
permalink: /gallery/
---

<style>
  .gallery-folder { margin-bottom: 2.5rem; }
  .gallery-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 1rem;
  }
  .gallery-item img {
    width: 100%;
    height: 140px;
    object-fit: cover;
    border-radius: 6px;
    display: block;
  }
  .gallery-item .caption {
    font-size: 0.75rem;
    word-break: break-all;
    margin-top: 0.25rem;
    color: #666;
  }
</style>

{% assign folders = site.data.image_gallery %}
{% for folder in folders %}
  {% assign folder_name = folder[0] %}
  {% assign files = folder[1] %}
  <div class="gallery-folder">
    <h2>{{ folder_name | default: "(top level)" }}</h2>
    <div class="gallery-grid">
      {% for file in files %}
        {% assign file_url = '/assets/images/' | append: file | relative_url %}
        <div class="gallery-item">
          <a href="{{ file_url }}" target="_blank">
            <img src="{{ file_url }}" alt="{{ file }}" loading="lazy">
          </a>
          <div class="caption">{{ file | split: '/' | last }}</div>
        </div>
      {% endfor %}
    </div>
  </div>
{% endfor %}
