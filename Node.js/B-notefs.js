/**
 * Node.js 文件模块
 */

const fs = require('fs');

/*
Part 1: 文件的整体读写
*/

function test_file_demo() {
  testfile = './testfs.txt';

  fs.writeFileSync(testfile, 'ABCDEF123456abcdef');

  // readFile: 根据参数读取文件内容，并激发callback函数
  // 该函数非阻塞（它不会阻止下面代码的运行）
  /*
  fs.readFile(testfile, 'utf8', function (err, data) {
    if(err != null)
      console.log('readFile failed');
    else
      console.log('readFile: ' + data);
  });
  */

  // readFileSync: 根据参数读取文件内容
  // 区别是：该函数会阻塞，读取完毕后结果写入变量
  let data = fs.readFileSync(testfile, 'utf8');
  if (data != null)
    console.log('readFileSync: ' + data);
  else
    console.log('readFileSync failed');

  // writeFile(Sync)也是相同的原理
  fs.writeFileSync(testfile, 'abcdef123456ABCDEF', 'utf8');

  /**
   * 文件描述符：
   *
   * 每个文件描述符唯一标识一个当前打开的文件。
   */

  console.log('Modified (before async): ' + fs.readFileSync(testfile, 'utf8'));

  // openSync: 同步打开一个文件，返回文件描述符fd
  fd = fs.openSync(testfile, 'a+');
  if (fd == null) {
    console.log('open: failed');
    return;
  }
  fs.writeSync(fd, '----', 12, 'utf8');
  fs.close(fd);

  console.log('Modified (after async): ' + fs.readFileSync(testfile, 'utf8'));

  // rmSync: 同步删除一个文件
  fs.rmSync(testfile);
}

/**
 * Part 2: 下面是黑马课程里一个课程成绩处理的示例。
 */

function course_score_demo() {
  course_score_data = [
    {'name' : 'Alex', 'score' : 85}, {'name' : 'Bob', 'score' : 93},
    {'name' : 'Cathy', 'score' : 92}, {'name' : 'Diana', 'score' : 90},
    {'name' : 'Eric', 'score' : 88}
  ]

  
}