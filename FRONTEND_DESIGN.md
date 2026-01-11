# Rethink Frontend Design & Features Documentation

## Project Overview

**Rethink** is a React-based Single Page Application (SPA) for tracking environmental impact metrics. The frontend communicates with a Django REST Framework backend via RESTful API endpoints.

**Tech Stack:**

- React 18.2.0
- React Router DOM 6.20.1
- Recharts 2.8.0 (data visualization)
- Lucide React (icons)
- CSS3 (custom styling, no framework)

**Base URL:** `http://localhost:8000/api/v1`

---

## Architecture & Project Structure

```
climatiqq-frontend/src/
├── App.js                 # Root component, routing, auth state management
├── App.css                # Global styles, utility classes
├── index.js               # React app entry point
├── components/
│   ├── Login.js          # User authentication (username/password)
│   ├── Login.css         # Login page styles
│   ├── Register.js       # User registration form
│   ├── Register.css      # Registration page styles
│   ├── Dashboard.js      # Main application interface
│   ├── Dashboard.css     # Dashboard styles
│   ├── Header.js          # Navigation header component
│   └── Header.css         # Header styles
└── services/
    └── api.js            # Centralized API service layer
```

---

## Authentication Flow

### Authentication State Management

**Location:** `App.js`

**State Variables:**

- `isAuthenticated` (boolean): Tracks if user is logged in
- `token` (string): JWT access token stored in localStorage
- `user` (object): Current user data (username, email)
- `isLoading` (boolean): Initial app load state

**Authentication Persistence:**

- Token stored in `localStorage.getItem('token')`
- On app load, checks localStorage for existing token
- If token exists, sets `isAuthenticated = true`
- Token included in all API requests via `Authorization: Bearer <token>` header

**Authentication Methods:**

- `handleLogin(newToken, userData)`: Sets auth state, stores token
- `handleLogout()`: Clears auth state, removes tokens from localStorage

### Protected Routes

**Route Protection Logic:**

- `/login` - Redirects to `/dashboard` if authenticated
- `/register` - Redirects to `/dashboard` if authenticated
- `/dashboard` - Redirects to `/login` if not authenticated
- `/` - Redirects to `/dashboard` if authenticated, else `/login`

---

## Component Specifications

### 1. App.js (Root Component)

**Purpose:** Application shell, routing, global state management

**Key Features:**

- React Router setup with BrowserRouter
- Global authentication state
- Route protection logic
- Loading spinner on initial app load
- Header component rendered on all routes

**State Management:**

```javascript
- isAuthenticated: boolean
- token: string | null
- user: object | null
- isLoading: boolean
```

**Routes:**

- `/login` → Login component
- `/register` → Register component
- `/dashboard` → Dashboard component (protected)
- `/` → Redirects based on auth status

---

### 2. Login.js Component

**Purpose:** User authentication interface

**Features:**

- Username/password login form
- Real-time error display
- Loading state during authentication
- Auto-redirect to dashboard on success
- Link to registration page
- Important notice about using username (not email)

**Form Fields:**

- `username` (text, required)
- `password` (password, required)

**State:**

```javascript
- formData: { username: string, password: string }
- error: string
- isLoading: boolean
```

**API Integration:**

- Calls `apiService.auth.login({ username, password })`
- Receives: `{ access: token, refresh: token, user: { username, email } }`
- Stores tokens in localStorage
- Calls parent `onLogin()` callback with token and user data

**User Experience:**

- Error messages clear when user types
- Form disabled during submission
- Button text changes to "Signing In..." during loading
- Navigates to `/dashboard` on successful login

---

### 3. Register.js Component

**Purpose:** New user registration

**Features:**

- Registration form with validation
- Password confirmation matching
- Real-time error display
- Loading state during registration
- Auto-login after successful registration
- Important notices about password reset and login method

**Form Fields:**

- `username` (text, required, minLength: 3, maxLength: 30)
- `email` (email, required)
- `password` (password, required, minLength: 8)
- `passwordConfirm` (password, required)

**Validation:**

- Client-side: Passwords must match
- Server-side: Username uniqueness, email uniqueness, password strength

**State:**

```javascript
- formData: { username, email, password, passwordConfirm }
- error: string
- isLoading: boolean
```

**API Integration:**

- Calls `apiService.auth.register({ username, email, password, passwordConfirm })`
- Receives: `{ access: token, refresh: token, user: { username, email }, message: string }`
- Stores tokens in localStorage
- Auto-navigates to dashboard

**Error Handling:**

- Displays field-specific errors from backend
- Shows user-friendly error messages
- Handles duplicate username/email errors

---

### 4. Header.js Component

**Purpose:** Global navigation header

**Features:**

- Rethink logo (custom CSS logo with "R" and leaves)
- Conditional navigation menu (only when authenticated)
- Dashboard link
- Logout button
- Fixed position at top of page

**Props:**

- `onLogout`: Function to handle logout
- `isAuthenticated`: Boolean to show/hide nav menu

**Styling:**

- Fixed header with z-index
- Logo is clickable link to dashboard
- Responsive design

---

### 5. Dashboard.js Component (Main Feature)

**Purpose:** Primary application interface for tracking environmental impact

**State Management:**

```javascript
- entries: Array<ImpactEntry>        // User's impact entries
- stats: Object                      // Calculated statistics from backend
- loading: boolean                   // Initial data load state
- filtering: boolean                 // Filter operation state (prevents full-page refresh)
- error: string                      // Error messages
- showAddModal: boolean              // Add entry modal visibility
- showDetailModal: boolean          // Entry detail modal visibility
- selectedEntry: ImpactEntry | null  // Currently selected entry
- filterMetric: string               // Current filter ("all" | "carbon" | "water" | "energy" | "digital")
- newEntry: { metric_type, value, description }  // Form data for new entry
```

**Key Features:**

#### A. Statistics Overview Cards

- **Total Carbon** (kg CO2) - from `stats.total_carbon`
- **Total Water** (L) - from `stats.total_water`
- **Total Energy** (kWh) - from `stats.total_energy`
- **Total Entries** - count of all entries

#### B. Advanced Data Visualizations (Recharts)

**1. Carbon Footprint - Radial Bar Chart**

- Progress ring showing percentage toward 1000 kg goal
- Displays: current total, goal percentage, average per entry, entry count
- Color: Green (#10b981)
- Icon: Wind (lucide-react)

**2. Water Usage - Treemap**

- Visual breakdown of water usage vs remaining (500L baseline)
- Shows: total used, remaining capacity
- Color: Cyan (#06b6d4)
- Icon: Droplets (lucide-react)

**3. Energy & Digital Impact - Scatter Chart**

- Bubble chart comparing energy vs digital metrics
- X-axis: Number of entries
- Y-axis: Average value
- Bubble size: Total value
- Colors: Yellow (energy), Purple (digital)
- Icon: Zap (lucide-react)

**4. Weekly Activity - Line Chart**

- Shows entry count per day of week (Sun-Sat)
- Calculated from entries' `created_at` timestamps
- Color: Indigo (#6366f1)
- Icon: Activity (lucide-react)

#### C. Entry Management

**Filtering:**

- Dropdown filter by metric type (All, Carbon, Water, Energy, Digital)
- Real-time filtering via API query parameter
- No full-page refresh (uses `filtering` state)
- Filter state persists during session

**Entry Display:**

- Grid layout of entry cards
- Each card shows:
  - Metric type icon (🌱💧⚡💻)
  - Metric type name (color-coded)
  - Value
  - Description
  - Created date
  - Delete button

**Add Entry:**

- Modal form with fields:
  - Metric type (dropdown: carbon, water, energy, digital)
  - Value (number, step: 0.01)
  - Description (textarea, optional)
- On submit: Creates entry, refreshes stats, closes modal
- Optimistic UI update (adds entry to list immediately)

**View Entry Details:**

- Click any entry card to view details modal
- Shows: metric type, value, description, created timestamp
- Modal overlay with close button

**Delete Entry:**

- Confirmation dialog before deletion
- Removes entry from list
- Refreshes statistics after deletion

#### D. Data Fetching Strategy

**Initial Load:**

- Fetches entries and stats in parallel using `Promise.all()`
- Shows full-page loading spinner
- Sets `loading = true`

**Filter Changes:**

- Only sets `filtering = true` (no full-page refresh)
- Disables filter dropdown during fetch
- Updates entries list smoothly

**After Add/Delete:**

- Refreshes stats to update visualizations
- Updates entries list

**API Calls:**

- `apiService.entries.getAll({ metric_type: filterMetric })` - Get filtered entries
- `apiService.stats.getImpactStats()` - Get calculated statistics
- `apiService.entries.create(entryData)` - Create new entry
- `apiService.entries.delete(id)` - Delete entry

#### E. Error Handling

- Displays error messages in error banner
- Errors clear on successful operations
- Console logging for debugging
- User-friendly error messages

#### F. Loading States

- **Initial Load:** Full-page loading spinner
- **Filtering:** Disabled dropdown, no visual spinner (smooth update)
- **Form Submission:** Disabled inputs, loading button text

---

## API Service Layer (api.js)

**Purpose:** Centralized HTTP client for all backend communication

### Architecture

**Class:** `ApiService`

- Singleton pattern (single instance exported)
- Base URL: `process.env.REACT_APP_API_URL || "http://localhost:8000/api/v1"`
- Automatic token injection in headers

### Methods

#### Generic Request Method

```javascript
async request(endpoint, options = {})
```

- Builds full URL from baseURL + endpoint
- Adds Authorization header if token exists
- Handles JSON parsing
- Error handling with DRF-compatible error extraction
- Returns parsed JSON or throws Error

**Error Handling:**

- Checks for `data.detail` or `data.error` (general errors)
- Extracts field-specific errors from response object
- Combines multiple errors into single message
- Throws Error with user-friendly message

#### Authentication Methods

```javascript
auth.register(userData); // POST /register/
auth.login(credentials); // POST /login/
auth.logout(); // POST /logout/
```

#### Entry Methods

```javascript
entries.getAll(filters); // GET /entries/?metric_type=carbon
entries.create(entryData); // POST /entries/
entries.getById(id); // GET /entries/<id>/
entries.update(id, data); // PUT /entries/<id>/
entries.delete(id); // DELETE /entries/<id>/
```

**Filter Support:**

- `getAll({ metric_type: "carbon" })` → `/entries/?metric_type=carbon`
- `getAll({})` or `getAll()` → `/entries/` (all entries)

#### Statistics Methods

```javascript
stats.getImpactStats(); // GET /stats/
```

**Returns:**

```json
{
  "total_entries": number,
  "recent_entries": number,
  "recent_activity": number,
  "metric_breakdown": [
    {
      "metric_type": "carbon",
      "total_value": number,
      "avg_value": number,
      "count": number
    }
  ]
}
```

---

## Styling Architecture

### Design System

**Color Palette:**

- Primary Green: `#10b981` (carbon, success)
- Blue: `#3b82f6` (water)
- Yellow: `#f59e0b` (energy)
- Purple: `#8b5cf6` (digital)
- Gray: `#6b7280` (neutral)
- Background: `#f8fafc` (light gray)

**Typography:**

- Font Family: System fonts (-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, etc.)
- Font Smoothing: Antialiased

**Spacing:**

- Consistent padding: 20px, 30px
- Card padding: 24px
- Grid gaps: 20px, 30px

**Border Radius:**

- Cards: 12px
- Buttons: 8px
- Inputs: 8px

**Shadows:**

- Cards: `0 2px 8px rgba(0, 0, 0, 0.1)`
- Hover: `0 4px 16px rgba(0, 0, 0, 0.15)`

### Component-Specific Styles

**App.css:**

- Global reset (margin, padding, box-sizing)
- Body styles
- Utility classes (text-center, mt-_, mb-_, p-\*)
- Button variants (primary, secondary, success, danger)
- Form styles (form-group, form-label, form-input)
- Alert styles (success, error, info)
- Responsive breakpoints (768px, 480px)

**Dashboard.css:**

- Dashboard container with gradient background
- Stats grid (responsive, auto-fit)
- Stat cards with hover effects
- Chart cards with advanced styling
- Entry cards with click handlers
- Modal overlays and content
- Filter controls styling
- Loading states

**Login/Register.css:**

- Centered card layout
- Custom logo styling (R with leaves)
- Form styling
- Error message styling
- Important notice boxes
- Link styling

**Header.css:**

- Fixed header positioning
- Logo styling
- Navigation menu
- Logout button

---

## Data Flow & State Management

### Authentication Flow

```
1. User enters credentials → Login.js
2. apiService.auth.login() → Backend API
3. Receives token + user data
4. Stores token in localStorage
5. Calls App.handleLogin()
6. Updates App state (isAuthenticated, token, user)
7. Navigates to /dashboard
```

### Dashboard Data Flow

```
1. Dashboard mounts → fetchData() called
2. Parallel API calls:
   - entries.getAll({ metric_type: filterMetric })
   - stats.getImpactStats()
3. Updates state: entries, stats
4. Renders:
   - Stats cards from stats object
   - Charts from stats.metric_breakdown
   - Entry cards from entries array
```

### Filter Flow

```
1. User selects filter → setFilterMetric(value)
2. useEffect detects filterMetric change
3. Checks if entries.length > 0 (not initial load)
4. Calls fetchData(true) with isFilterChange flag
5. Sets filtering = true (disables dropdown)
6. API call with query parameter
7. Updates entries state
8. Sets filtering = false
9. UI updates smoothly (no full-page refresh)
```

### Add Entry Flow

```
1. User clicks "Add New Entry" → setShowAddModal(true)
2. User fills form → updates newEntry state
3. User submits → handleAddEntry()
4. apiService.entries.create(newEntry)
5. Optimistically adds to entries list
6. Refreshes stats
7. Closes modal, resets form
```

### Delete Entry Flow

```
1. User clicks Delete → window.confirm()
2. If confirmed → apiService.entries.delete(id)
3. Filters entry from entries array
4. Refreshes stats
5. UI updates
```

---

## User Interactions & UX Patterns

### Form Interactions

- **Real-time validation:** Errors clear when user types
- **Loading states:** Buttons show loading text, inputs disabled
- **Error display:** Red error messages above submit button
- **Success feedback:** Auto-navigation on success

### Modal Patterns

- **Overlay click:** Click outside modal closes it
- **Close button:** X button in header
- **Escape key:** (Not implemented, but standard pattern)
- **Form submission:** Closes modal on success

### Entry Card Interactions

- **Click card:** Opens detail modal
- **Click delete:** Shows confirmation, deletes entry
- **Hover effects:** Cards lift slightly on hover

### Filter Interactions

- **Dropdown change:** Immediately triggers API call
- **Loading state:** Dropdown disabled during fetch
- **Smooth update:** No page refresh, entries update in place

### Chart Interactions

- **Tooltips:** Hover shows detailed data
- **Responsive:** Charts resize with container
- **Color coding:** Each metric has consistent color

---

## Error Handling Strategy

### API Error Handling

1. **Network errors:** Caught in try/catch, displayed to user
2. **HTTP errors:** Extracted from response, user-friendly messages
3. **Validation errors:** Field-specific errors combined into single message
4. **Authentication errors:** Redirects to login (if implemented)

### User-Facing Errors

- **Login/Register:** Error message below form
- **Dashboard:** Error banner at top of stats section
- **Entry operations:** Error message in modal or banner

### Error Message Format

- Backend returns: `{ "username": ["Error message"] }`
- Frontend extracts: "Error message"
- Multiple errors: Combined with ". " separator

---

## Performance Optimizations

### Data Fetching

- **Parallel requests:** Entries and stats fetched simultaneously
- **Conditional fetching:** Filter only fetches if entries exist
- **Optimistic updates:** UI updates before API confirmation

### Rendering

- **useCallback:** fetchData memoized to prevent unnecessary re-renders
- **Conditional rendering:** Charts only render if data exists
- **Lazy loading:** (Not implemented, but charts could be lazy-loaded)

### State Management

- **Separate loading states:** `loading` for initial, `filtering` for filters
- **Prevents unnecessary renders:** useCallback dependencies carefully managed

---

## Responsive Design

### Breakpoints

- **Desktop:** Default (1200px max-width)
- **Tablet:** 768px and below
- **Mobile:** 480px and below

### Responsive Features

- **Grid layouts:** Auto-fit columns (minmax)
- **Padding:** Reduces on smaller screens
- **Font sizes:** Adjusts for readability
- **Charts:** ResponsiveContainer adapts to screen size

---

## Accessibility Considerations

### Current Implementation

- **Form labels:** All inputs have associated labels
- **Button text:** Descriptive (not just icons)
- **Error messages:** Visible and clear
- **Loading states:** Disabled inputs prevent double-submission

### Areas for Improvement

- ARIA labels for icons
- Keyboard navigation for modals
- Focus management
- Screen reader announcements

---

## Security Features

### Token Management

- **Storage:** localStorage (persists across sessions)
- **Injection:** Automatic in API service headers
- **Cleanup:** Removed on logout

### Input Validation

- **Client-side:** HTML5 validation (required, minLength, type)
- **Server-side:** Backend validation (trust backend)

### XSS Prevention

- React automatically escapes content
- No dangerouslySetInnerHTML used

---

## Future Enhancement Opportunities

### Features Not Yet Implemented

1. **Update Entry:** Backend supports PUT, frontend UI not implemented
2. **Date Range Filtering:** Backend ready, frontend UI needed
3. **Export Data:** CSV/JSON export functionality
4. **User Profile:** Profile viewing/editing
5. **Password Reset:** Currently shows notice, not implemented
6. **Search:** Text search within entries
7. **Pagination:** For large entry lists
8. **Sorting:** Sort entries by date, value, type

### Technical Improvements

1. **Error Boundaries:** React error boundaries for better error handling
2. **Context API:** For global state management
3. **React Query:** For better data fetching/caching
4. **TypeScript:** Type safety
5. **Testing:** Unit tests, integration tests
6. **PWA:** Service workers, offline support

---

## Key Design Decisions

### Why React Router?

- Client-side routing for SPA
- Protected routes with authentication
- Clean URL structure

### Why Recharts?

- React-native charting library
- Responsive by default
- Good documentation
- Multiple chart types

### Why Custom CSS?

- No framework dependencies
- Full control over styling
- Smaller bundle size
- Learning opportunity

### Why Centralized API Service?

- Single source of truth for API calls
- Consistent error handling
- Easy to update endpoints
- Token management in one place

### Why localStorage for Tokens?

- Persists across sessions
- Simple implementation
- No server-side session needed
- Works with JWT stateless auth

---

## Component Dependencies

```
App.js
├── React Router (BrowserRouter, Routes, Route, Navigate)
├── Header.js
├── Login.js
│   └── apiService.auth.login()
├── Register.js
│   └── apiService.auth.register()
└── Dashboard.js
    ├── Recharts (multiple chart components)
    ├── Lucide React (icons)
    └── apiService (entries, stats)
```

---

## API Endpoint Mapping

| Frontend Method                 | HTTP Method | Endpoint                       | Purpose                   |
| ------------------------------- | ----------- | ------------------------------ | ------------------------- |
| `auth.register()`               | POST        | `/register/`                   | Create new user           |
| `auth.login()`                  | POST        | `/login/`                      | Authenticate user         |
| `auth.logout()`                 | POST        | `/logout/`                     | Logout user               |
| `entries.getAll()`              | GET         | `/entries/`                    | Get all entries           |
| `entries.getAll({metric_type})` | GET         | `/entries/?metric_type=carbon` | Get filtered entries      |
| `entries.create()`              | POST        | `/entries/`                    | Create new entry          |
| `entries.getById()`             | GET         | `/entries/<id>/`               | Get single entry          |
| `entries.update()`              | PUT         | `/entries/<id>/`               | Update entry              |
| `entries.delete()`              | DELETE      | `/entries/<id>/`               | Delete entry              |
| `stats.getImpactStats()`        | GET         | `/stats/`                      | Get calculated statistics |

---

## Data Structures

### ImpactEntry Object

```typescript
{
  id: number
  metric_type: "carbon" | "water" | "energy" | "digital"
  value: number
  description: string
  created_at: string (ISO datetime)
  user: number (user ID)
}
```

### Stats Object

```typescript
{
	total_entries: number;
	recent_entries: number;
	recent_activity: number;
	metric_breakdown: Array<{
		metric_type: string;
		total_value: number;
		avg_value: number;
		count: number;
	}>;
}
```

### User Object

```typescript
{
	username: string;
	email: string;
}
```

---

## Environment Configuration

**Environment Variables:**

- `REACT_APP_API_URL`: Backend API base URL (defaults to `http://localhost:8000/api/v1`)

**Usage:**

- Set in `.env` file in frontend root
- Accessed via `process.env.REACT_APP_API_URL`
- Must be prefixed with `REACT_APP_` to be accessible in React

---

## Build & Deployment

**Development:**

- `npm start` - Runs on `http://localhost:3000`
- Hot reload enabled
- Source maps for debugging

**Production:**

- `npm run build` - Creates optimized build
- Output: `build/` directory
- Static files ready for deployment

**Dependencies:**

- See `package.json` for full list
- Key: react, react-dom, react-router-dom, recharts, lucide-react

---

## Testing Strategy (Recommended)

### Unit Tests

- Component rendering
- State management
- Form validation
- API service methods

### Integration Tests

- Authentication flow
- Entry CRUD operations
- Filter functionality
- Chart data rendering

### E2E Tests

- Complete user journeys
- Login → Add Entry → View Stats → Logout

---

## Conclusion

This frontend is a **production-ready MVP** with:

- ✅ Complete authentication flow
- ✅ Full CRUD for entries
- ✅ Advanced data visualizations
- ✅ Real-time filtering
- ✅ Responsive design
- ✅ Error handling
- ✅ Loading states
- ✅ User-friendly UX

The architecture is **scalable** and **maintainable**, with clear separation of concerns and centralized API management.
