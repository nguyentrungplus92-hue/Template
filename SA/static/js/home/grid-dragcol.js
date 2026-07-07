/* ============================================================
   grid-dragcol.js - Kéo-thả đổi thứ tự cột cho bảng .grid
   Client-side, nhớ trong phiên (tải lại trang -> về mặc định).
   Tự chạy cho mọi <table class="grid"> có class "draggable-cols".
   ============================================================ */
(function () {
    'use strict';

    function initTable(table) {
        var thead = table.tHead;
        if (!thead) return;
        var headRow = thead.rows[0];
        if (!headRow) return;

        var dragSrcIndex = null;

        // Gắn kéo-thả cho từng ô tiêu đề
        Array.prototype.forEach.call(headRow.cells, function (th, index) {
            th.setAttribute('draggable', 'true');
            th.classList.add('col-draggable');

            th.addEventListener('dragstart', function (e) {
                dragSrcIndex = index;
                th.classList.add('col-dragging');
                e.dataTransfer.effectAllowed = 'move';
                // Firefox cần setData mới cho kéo
                try { e.dataTransfer.setData('text/plain', String(index)); } catch (x) {}
            });

            th.addEventListener('dragend', function () {
                th.classList.remove('col-dragging');
                clearMarkers(headRow);
            });

            th.addEventListener('dragover', function (e) {
                e.preventDefault();
                e.dataTransfer.dropEffect = 'move';
                clearMarkers(headRow);
                // Đánh dấu vị trí sẽ thả (viền trái)
                th.classList.add('col-drop-target');
            });

            th.addEventListener('dragleave', function () {
                th.classList.remove('col-drop-target');
            });

            th.addEventListener('drop', function (e) {
                e.preventDefault();
                clearMarkers(headRow);
                var targetIndex = index;
                if (dragSrcIndex === null || dragSrcIndex === targetIndex) return;
                moveColumn(table, dragSrcIndex, targetIndex);
                dragSrcIndex = null;
            });
        });
    }

    function clearMarkers(headRow) {
        Array.prototype.forEach.call(headRow.cells, function (th) {
            th.classList.remove('col-drop-target');
        });
    }

    // Di chuyển cột từ vị trí from -> to ở HEADER và MỌI dòng dữ liệu
    function moveColumn(table, from, to) {
        moveCellInRow(table.tHead.rows[0], from, to);
        Array.prototype.forEach.call(table.tBodies, function (tbody) {
            Array.prototype.forEach.call(tbody.rows, function (row) {
                // Bỏ qua dòng đặc biệt (vd dòng "không có dữ liệu" dùng colspan)
                if (row.cells.length === table.tHead.rows[0].cells.length) {
                    moveCellInRow(row, from, to);
                }
            });
        });
    }

    // Chuyển 1 ô trong 1 hàng từ vị trí from sang to
    function moveCellInRow(row, from, to) {
        var cell = row.cells[from];
        if (!cell) return;
        if (from < to) {
            // chèn sau ô đích
            row.insertBefore(cell, row.cells[to].nextSibling);
        } else {
            // chèn trước ô đích
            row.insertBefore(cell, row.cells[to]);
        }
    }

    // Khởi động khi trang tải xong
    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('table.grid.draggable-cols').forEach(initTable);
    });
})();
