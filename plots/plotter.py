class StatPlotter:

    def get_plot_string(self, columns_names, rows, x_title, y_title):
        out_text = """<script type="text/javascript">
        google.charts.load('current', {packages: ['corechart', 'line']});
        google.charts.setOnLoadCallback(drawLineColors);"""
        out_text += "\n"

        out_text += """        function drawLineColors() {
            var data = new google.visualization.DataTable();"""

        for column_name in columns_names:
            out_text += "data.addColumn('number','" + column_name + "');\n"

        out_text += "data.addRows(["
        for row in rows:
            out_text += str(row) + ",\n"

        out_text += "]);\n"

        out_text += """var options = 
            {
                hAxis:
                {
                    title: """
        out_text += "'" + x_title + "'\n"
        out_text += """},
                vAxis: 
                {
                    title: """
        out_text += "'" + y_title + "'\n"
        out_text += """ },
                colors: ['#a52714', '#097138'],
                backgroundColor: '#333'
            };

            var chart = new google.visualization.LineChart(document.getElementById('main-plot'));
            chart.draw(data, options);
        }
        </script>"""
        return out_text


if __name__ == "__main__":
    c_names = ["X", "Dogs", "Cats"]
    data_rows = [[0, 0, 0], [1, 10, 5], [2, 23, 15], [3, 17, 9], [4, 18, 10], [5, 9, 5],
                 [6, 11, 3], [7, 27, 19], [8, 33, 25], [9, 40, 32], [10, 32, 24], [11, 35, 27],
                 [12, 30, 22], [13, 40, 32], [14, 42, 34], [15, 47, 39], [16, 44, 36], [17, 48, 40],
                 [18, 52, 44], [19, 54, 46], [20, 42, 34], [21, 55, 47], [22, 56, 48], [23, 57, 49],
                 [24, 60, 52], [25, 50, 42], [26, 52, 44], [27, 51, 43], [28, 49, 41], [29, 53, 45],
                 [30, 55, 47], [31, 60, 52], [32, 61, 53], [33, 59, 51], [34, 62, 54], [35, 65, 57],
                 [36, 62, 54], [37, 58, 50], [38, 55, 47], [39, 61, 53], [40, 64, 56], [41, 65, 57],
                 [42, 63, 55], [43, 66, 58], [44, 67, 59], [45, 69, 61], [46, 69, 61], [47, 70, 62],
                 [48, 72, 64], [49, 68, 60], [50, 66, 58], [51, 65, 57], [52, 67, 59], [53, 70, 62],
                 [54, 71, 63], [55, 72, 64], [56, 73, 65], [57, 75, 67], [58, 70, 62], [59, 68, 60],
                 [60, 64, 56], [61, 60, 52], [62, 65, 57], [63, 67, 59], [64, 68, 60], [65, 69, 61],
                 [66, 70, 62], [67, 72, 64], [68, 75, 67], [69, 80, 72]]
    x_title = "Time"
    y_title = "Popularity"

    plotter = StatPlotter()
    text = plotter.get_plot_string(c_names, data_rows, x_title, y_title)
    print(text)
