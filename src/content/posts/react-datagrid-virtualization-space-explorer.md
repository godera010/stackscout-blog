---
title: "Virtualizing 100,000 Rows at 60 FPS: Building a Space Mission Explorer with React DataGrid"
description: "A deep dive into React DataGrid performance and architecture: rendering 100,000+ records at 60 FPS using DOM virtualization, tree hierarchies, and memoized cell renderers."
date: 2026-08-25
tags: ["React", "Performance", "Frontend", "Virtualization"]
tldr: "Rendering large tabular datasets in React without DOM virtualization crashes browser memory and drops frame rates below usable thresholds. Using React DataGrid (`@inovua/reactdatagrid-community`), you can render 100,000+ records at a stable 60 FPS with nested tree hierarchies, faceted sorting, and instant keyboard navigation."
image: ../../assets/images/react_datagrid_virtualization.jpg
imageAlt: "React data grid virtualization diagram"
---

## Why Standard HTML Tables Choke on 10,000+ Rows

When you render a standard `<table>` in React with 10,000 rows and 8 columns, you mount 80,000 individual DOM nodes. The browser engine has to calculate layout geometry, font metrics, and event listeners for all 80,000 elements simultaneously.

The result is immediate UI degradation:
- Scroll frame rates drop from 60 FPS to under 12 FPS.
- Browser tab memory climbs past 450MB.
- Filtering or sorting triggers 800ms+ main-thread freezes.

The fix is DOM virtualization: keeping only the 25–40 rows currently inside the viewport mounted in the DOM.

```
┌────────────────────────────────────────────────────────┐
│               React DataGrid Viewport                  │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Mounted DOM Slice (Rows 104–130 Visible)         │  │
│  └──────────────────────────────────────────────────┘  │
│                                                        │
│  Virtual Window Buffer (Top / Bottom CSS Transform)    │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│     In-Memory / Server-Side Store (100,000 Records)     │
└────────────────────────────────────────────────────────┘
```

## How Viewport Virtualization Keeps DOM Node Counts Under 100

React DataGrid calculates the scroll container's pixel offset on each animation frame. It positions mounted rows using absolute CSS transforms while recycling unmounted DOM nodes as the user scrolls.

Three features make it particularly effective for dense datasets:
1. **Row and Column Virtualization:** It virtualizes horizontally as well as vertically, making 50-column datasets as fast as 5-column ones.
2. **Native Tree Data Support:** It handles parent-child mission stages (e.g., *Apollo 11* → *Launch* → *Translunar Injection* → *Lunar Landing*) without requiring third-party state managers.
3. **Memoized Cell Renderers:** High-frequency cell updates avoid triggering full table reconciliation passes.

## Step-by-Step Implementation: The Space Mission Explorer

### Step 1: Install Dependencies
Install the community package:

```bash
npm install @inovua/reactdatagrid-community
```

### Step 2: Define Columns with Strict Formatting
Always define columns outside the component or wrap them in `useMemo` to prevent unnecessary table re-renders:

```tsx
import React, { useMemo, useState } from 'react';
import ReactDataGrid from '@inovua/reactdatagrid-community';
import '@inovua/reactdatagrid-community/index.css';
import '@inovua/reactdatagrid-community/theme/default-dark.css';

interface MissionRecord {
  id: string;
  missionName: string;
  agency: string;
  costMillions: number;
  status: 'SUCCESS' | 'FAILURE' | 'ACTIVE';
  launchDate: string;
}

export function SpaceMissionExplorer({ data }: { data: MissionRecord[] }) {
  const [selectedRow, setSelectedRow] = useState<MissionRecord | null>(null);

  const columns = useMemo(() => [
    { name: 'id', header: 'Mission ID', defaultWidth: 120 },
    { name: 'missionName', header: 'Mission Name', minWidth: 200, defaultFlex: 2 },
    { name: 'agency', header: 'Agency', minWidth: 140, defaultFlex: 1 },
    { 
      name: 'costMillions', 
      header: 'Budget ($M)', 
      type: 'number', 
      defaultWidth: 130,
      render: ({ value }: { value: number }) => `$${value.toLocaleString()}`
    },
    { 
      name: 'status', 
      header: 'Status', 
      defaultWidth: 120,
      render: ({ value }: { value: string }) => (
        <span className={`status-pill status-${value.toLowerCase()}`}>
          {value}
        </span>
      )
    },
    { name: 'launchDate', header: 'Launch Date', defaultWidth: 140 }
  ], []);

  return (
    <div style={{ height: 600, width: '100%' }}>
      <ReactDataGrid
        idProperty="id"
        theme="default-dark"
        style={{ height: '100%', width: '100%' }}
        columns={columns}
        dataSource={data}
        pagination
        defaultLimit={50}
        virtualizeColumns
        enableSelection
        onSelectionChange={({ data }) => setSelectedRow(data as MissionRecord)}
      />
    </div>
  );
}
```

## Comparison: React Data Grid Options

| Dimension | React DataGrid (@inovua) | AG Grid (Community) | TanStack Table (v8) |
| :--- | :--- | :--- | :--- |
| **Model** | Turnkey Component | Enterprise Framework | Headless UI Hook |
| **Virtualization** | Built-in (Rows & Columns) | Built-in | Requires `@tanstack/react-virtual` |
| **Tree Data** | Native Support | Community Partial | Manual state mapping |
| **Out-of-the-Box Dark Theme**| Yes | Yes | None (Build your own CSS) |
| **Bundle Size** | ~140 KB | ~320 KB | ~15 KB (Headless only) |

## Performance Mistakes to Avoid

- **Defining Columns Inside Render:** Instantiating column arrays inside component bodies breaks reference equality and triggers a full grid layout recomputation on every keystroke.
- **Un-memoized Custom Cell Renderers:** Inline functions in `render` props force cell reconciliation on every scroll tick.
- **Client-Side Sorting on 1M+ Records:** When datasets exceed 20,000 rows, offload sorting and filtering to SQL queries via backend pagination endpoints.

## Frequently Asked Questions

### How does React DataGrid maintain 60 FPS on 100,000 rows?
It uses DOM virtualization to render only the visible viewport rows (typically 20–40 nodes), keeping browser layout calculations constant regardless of total dataset size.

### What is the difference between React DataGrid and TanStack Table?
TanStack Table is a headless library providing data logic without UI elements, while React DataGrid is a complete component with pre-built virtualization, theming, and controls.

### Can React DataGrid render expandable tree hierarchies?
Yes. React DataGrid natively supports Tree Data structures, allowing hierarchical parent-child records to expand and collapse without custom state wrappers.

### Does React DataGrid support column virtualization?
Yes. Setting `virtualizeColumns` ensures tables with dozens of columns only mount visible horizontal cells, preventing layout recalculation lag.

### How do you export data from React DataGrid to CSV?
React DataGrid provides built-in export utilities that extract filtered, sorted, and grouped table data directly into CSV or Excel XLSX files.

## Conclusion & Key Takeaways

For applications requiring dense, real-time data grids with virtualization and tree support, React DataGrid delivers enterprise performance with minimal configuration. Keep columns memoized, enable viewport virtualization, and let the engine handle the rest.
