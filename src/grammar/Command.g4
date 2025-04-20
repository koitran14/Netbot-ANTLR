grammar Command;

command: xinchao (goimon | naptien) | xinchao ;          // Quy tắc gốc: các loại lệnh
xinchao: command;
goimon: food | drink;

// food
goimon: 'đặt' 'lịch' 'hẹn' 'vào' ('ngày')? day 'lúc' time ;  // Lệnh đặt lịch
cancel: 'hủy' 'lịch' 'hẹn' 'vào' day ;              // Lệnh hủy lịch
day: 'thứ Hai' | 'thứ Ba' | 'thứ Tư' | 'thứ Năm' | 'thứ Sáu' | 'thứ Bảy' | 'Chủ Nhật' ;
time: NUMBER ('giờ' | 'h') ('sáng' | 'chiều')? ;            // Giờ (ví dụ: 10 giờ sáng)
NUMBER: [0-9]+ ;                                    // Số nguyên

//drink

//naptien


WS: [ \t\r\n]+ -> skip ;                            // Bỏ qua khoảng trắng
