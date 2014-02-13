$(document).ready(function() {
  var max_nodes = 75;
  var datagrepper_base_url = 'http://127.0.0.1:5000';
  //var datagrepper_base_url = 'https://apps.fedoraproject.org/datagrepper';
  var w = 800,
      h = 600;

  var force = d3.layout.force()
  var svg = d3.select("#logo-container").append("svg:svg")
      .attr("width", w)
      .attr("height", h);

  var nodes = [];
  var links = [];

  force
    .nodes(nodes)
    .links(links)
    .size([w, h])
    .linkDistance(60)
    .charge(-100)
    .start();

  var node_base = svg.append("svg:g");
  var path_base = svg.append("svg:g");

  var update = function() {
    var node = node_base.selectAll(".node")
        .data(force.nodes())
      .enter()
        .append("g").attr("class", "node")
        .call(force.drag);

    var path = path_base.selectAll("path")
        .data(force.links())
      .enter()
        .append("svg:path")
        .attr("class", "link");

    node_base.selectAll(".node").data(force.nodes()).exit().remove();

    node
        .append("svg:circle")
        .attr('color', 'black')
        .attr('r', function (d) { return d.relevance });


    function tick() {
      path_base.selectAll("path")
          .attr("d", function(d) {
            var dx = d.target.x - d.source.x,
                dy = d.target.y - d.source.y,
                dr = Math.sqrt(dx * dx + dy * dy);
            return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
          });

      node_base.selectAll(".node").attr("transform", function(d) {
        return "translate(" + d.x + "," + d.y + ")";
      });
    }

    force.on('tick', tick);
    force.start();
  }
  var create_node = function(id) {
    nodes.push({
      x: (w / 2) + (Math.random() - 0.5) * (w / 8),
      y: (h / 2) + (Math.random() - 0.5) * (w / 8),
      name: id,
      id: id,
      relevance: 2
    });
    return nodes.length - 1;
  };
  var bump_node = function(index) {
      var node = nodes[index];
      /* For some reason this isn't working... */
      /*
      node['relevance'] = node['relevance'] + 6;
      var decay = function() {
          if (node['relevance'] > 2) {
              node['relevance'] = node['relevance'] - 1;
              setTimeout(decay, 500);
          }
      }
      setTimeout(decay, 1000);
     */
  }
  var datagrepper_callback = function(json, page) {
      var worker = function(i, modname, j, path) {
          var tokens = path.split('/');
          for (var k = 0; k < tokens.length; k++ ) {
              var id = modname;
              for (var l = 0; l < k - 1; l++) {
                  id = id + "/" + tokens[l];
              }
              var parent_id = id;
              if (k > 0) {
                  id = id + "/" + tokens[k - 1];
              }

              var parent_i = find_node_by_id(parent_id);
              if (parent_i === undefined) {
                  parent_i = create_node(id);
              }
              var node_i = find_node_by_id(id);
              if (node_i === undefined) {
                  node_i = create_node(id);
              }

              // No need to link in the case that these are the same.
              if (parent_i == node_i) {
                  continue;
              }

              // Draw attention to this node.
              bump_node(node_i);

              var link_i = find_link_by_indices(parent_i, node_i);
              if (link_i === undefined) {
                  links.push({
                      "source": parent_i,
                      "target": node_i,
                  })
              } else {
                  // Pass.  link already exists.
              }
          }
          update();

      }
      $.each(json.raw_messages, function(i, message) {
          $("#timestamp").html(message.meta.date);
          $("#history").append(
              "<li class='list-group-item'>" +
              message.meta.subtitle +
              "</li>"
          );
          var modname = message.topic.split('.')[3];
          $.each(message.meta.objects, function(j, path) {
              worker(i, modname, j, path);
          });
      });
      if (page < 80) {
          setTimeout(function() {
              load_page(page + 1);
          }, 100);
      } else {
          $("#status").html("Done.");
      }
  };

  var load_page = function(page) {
      var meta_args = '?meta=subtitle&meta=objects&meta=date';
      $.ajax(datagrepper_base_url + '/raw/' + meta_args, {
          data: {
              order: 'asc',
              rows_per_page: 20,
              page: page,
          },
          dataType: "jsonp",
          success: function(json) { datagrepper_callback(json, page) },
          error: function() {
              console.log(arguments);
          }
      });
  };

  var find_node_by_id = function(id) {
      for (var i = 0; i < nodes.length; i++) {
          if (nodes[i].id == id) {
              return i;
          }
      }
      return undefined;
  }
  var find_link_by_indices = function(parent_i, node_i) {
      for (var i = 0; i < links.length; i++) {
          if (links[i].source.index == parent_i &&
              links[i].target.index == node_i) {
              return i;
          }
      }
      return undefined;
  }
  var remove_oldest_child_node = function() {

      if (nodes.length < max_nodes) {
          setTimeout(remove_oldest_child_node, 1000);
          return;
      } else {
          setTimeout(remove_oldest_child_node, 1);
      }

      var target_node_i = undefined;
      for (var i = 0; i < nodes.length; i++) {
          var is_a_parent = false;
          for (var j = 0; j < links.length; j++) {
              if (links[j].source.index == i) {
                  is_a_parent = true;
                  break;
              }
          }
          if (is_a_parent) {
              continue;
          }
          target_node_i = i;
          break
      }

      if (target_node_i != undefined) {
          nodes.splice(target_node_i, 1);
      } else {
          console.log('could not find a child node');
      }

      for (var i = 0; i < links.length; i++) {
          if (links[i].target.index == target_node_i) {
              links.splice(i, 1);
              i = i - 1;
          }
      }
      update();
  }
  $("#status").html("Loading datagrepper history...");
  load_page(1);
  setTimeout(remove_oldest_child_node, 1000);
  //setTimeout(function() {
  //    console.log(nodes);
  //}, 1000);
});
