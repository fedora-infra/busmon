<%inherit file="busmon.templates.master"/>
<div class="page">
  <div class="left pane">
    <div class="content">
      <strong>Messages per Topic</strong>
      ${barchart.display() | n}
    </div>
    <div class="clear spacer"></div>
    <div class="content">
      <strong>Total Messages over Time</strong>
      ${timeseries.display() | n}
    </div>
  </div>
  <div class="right pane">
    <div class="content">
      <strong>Last 5 Messages</strong>
      ${colorized_messages.display() | n}
    </div>
  </div>
</div>
