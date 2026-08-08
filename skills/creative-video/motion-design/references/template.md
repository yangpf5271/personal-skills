# 动效设计参考

## 缓动曲线速查
| 用途 | 曲线 | CSS |
|------|------|-----|
| 元素进入 | ease-out | cubic-bezier(0,0,0.2,1) |
| 元素退出 | ease-in | cubic-bezier(0.4,0,1,1) |
| 标准转场 | ease-in-out | cubic-bezier(0.4,0,0.2,1) |
| 弹性效果 | spring | linear() 或 JS spring |

## 时长速查
| 类型 | 时长 | 示例 |
|------|------|------|
| 微交互 | 100-200ms | 按钮hover、图标切换 |
| 小转场 | 200-300ms | 卡片展开、tooltip |
| 中转场 | 300-500ms | 页面切换、modal |
| 大转场 | 500-700ms | 路由切换、hero动画 |

## 无障碍
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; }
}
```