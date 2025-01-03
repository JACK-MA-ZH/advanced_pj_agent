module register (
    input wire clk,          // 时钟信号
    input wire reset,        // 复位信号
    input wire [7:0] d,     // 输入数据
    output reg [7:0] q       // 输出数据
);

always @(posedge clk or posedge reset) begin
    if (reset) begin
        q <= 8'b0;          // 当复位时，输出为 0
    end else begin
        q <= d;             // 在时钟上升沿时，更新输出
    end
end

endmodule