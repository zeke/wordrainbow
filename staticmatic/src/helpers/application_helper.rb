module ApplicationHelper

  def link_to_function(name, function, opts={})
    opts = opts.merge({:onclick => "javascript:#{function};return false;"})
    link(name, "#", opts)
  end

end