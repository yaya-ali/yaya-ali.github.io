#!/usr/bin/env ruby
#
# Builds a GitHub-style contribution heatmap from THIS repo's own commit
# history (not the GitHub-wide API), exposed as site.data.commit_activity.
# Runs at build time — accurate locally and in the Pages Actions build
# (checkout uses fetch-depth: 0, so full history is present).

require "date"

module Jekyll
  class GitHeatmapGenerator < Generator
    priority :high

    def generate(site)
      today = Date.today
      # 53 weeks back, snapped to the Sunday that starts that week
      start = today - (53 * 7)
      start -= start.wday # 0 = Sunday

      counts = Hash.new(0)
      log = `git -C "#{site.source}" log --since="#{start.iso8601}" --pretty=%ad --date=short 2>/dev/null`
      log.each_line do |line|
        d = line.strip
        counts[d] += 1 unless d.empty?
      end

      days = []
      (start..today).each do |d|
        c = counts[d.to_s]
        level =
          if    c == 0 then 0
          elsif c <= 1 then 1
          elsif c <= 3 then 2
          elsif c <= 5 then 3
          else 4
          end
        days << { "date" => d.to_s, "count" => c, "level" => level }
      end

      site.data["commit_activity"] = {
        "days"        => days,
        "total"       => counts.values.sum,
        "active_days" => counts.size
      }
    end
  end
end
