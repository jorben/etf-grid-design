/**
 * 检查未使用的导入脚本
 * 用于识别项目中未使用的导入语句
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const srcDir = path.join(__dirname, '../src');

function checkUnusedImports() {
  const files = getAllFiles(srcDir);
  
  console.log('检查未使用的导入...\n');
  
  files.forEach(file => {
    if (file.endsWith('.jsx') || file.endsWith('.js')) {
      checkFileImports(file);
    }
  });
}

function getAllFiles(dir) {
  let results = [];
  const list = fs.readdirSync(dir);
  
  list.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat && stat.isDirectory()) {
      results = results.concat(getAllFiles(filePath));
    } else {
      results.push(filePath);
    }
  });
  
  return results;
}

function checkFileImports(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n');
    const imports = [];
    const usedIdentifiers = new Set();
    
    // 提取导入的标识符
    lines.forEach((line, index) => {
      const importMatch = line.match(/import\s+(?:{([^}]+)}|\*\s+as\s+(\w+)|\w+)\s+from\s+['"]([^'"]+)['"]/);
      if (importMatch) {
        if (importMatch[1]) {
          // 命名导入 {a, b, c}
          const namedImports = importMatch[1].split(',').map(s => s.trim().split(' as ')[0]);
          imports.push(...namedImports.map(name => ({ name, line: index + 1 })));
        } else if (importMatch[2]) {
          // 命名空间导入 * as something
          imports.push({ name: importMatch[2], line: index + 1 });
        } else {
          // 默认导入
          const defaultImport = line.match(/import\s+(\w+)/);
          if (defaultImport) {
            imports.push({ name: defaultImport[1], line: index + 1 });
          }
        }
      }
      
      // 收集使用的标识符
      imports.forEach(imp => {
        if (line.includes(imp.name) && !line.includes('import')) {
          usedIdentifiers.add(imp.name);
        }
      });
    });
    
    // 找出未使用的导入
    const unusedImports = imports.filter(imp => !usedIdentifiers.has(imp.name));
    
    if (unusedImports.length > 0) {
      console.log(`文件: ${path.relative(srcDir, filePath)}`);
      unusedImports.forEach(imp => {
        console.log(`  第${imp.line}行: 未使用的导入 "${imp.name}"`);
      });
      console.log('');
    }
  } catch (error) {
    console.error(`处理文件 ${filePath} 时出错:`, error.message);
  }
}

checkUnusedImports();