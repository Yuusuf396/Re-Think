# MVP Status & Requirements

## 🎯 What is an MVP?

**Minimum Viable Product (MVP)**: The simplest version of your product that can be used by real users to accomplish the core goal.

For Climatiqq, the MVP should allow users to:
1. ✅ Register an account
2. ✅ Log in
3. ✅ Create environmental impact entries
4. ✅ View their entries
5. ✅ See basic statistics
6. ✅ Delete entries
7. ⚠️ Update entries (backend ready, frontend missing)

---

## ✅ What's Currently Implemented

### Backend (Django REST API) - **FULLY FUNCTIONAL**

#### Authentication ✅
- **Registration**: `POST /api/v1/register/`
  - Accepts: username, email, password, password_confirm
  - Returns: JWT tokens + user info
  - Status: ✅ **WORKING**

- **Login**: `POST /api/v1/login/`
  - Accepts: email (as username), password
  - Returns: JWT tokens
  - Status: ✅ **WORKING**

- **JWT Authentication**: 
  - Token expiry: 24 hours
  - All protected endpoints require valid token
  - Status: ✅ **WORKING**

#### Impact Entries API ✅
- **List Entries**: `GET /api/v1/entries/`
  - Returns: All entries for authenticated user
  - Status: ✅ **WORKING**

- **Create Entry**: `POST /api/v1/entries/`
  - Accepts: metric_type, value, description
  - Returns: Created entry
  - Status: ✅ **WORKING**

- **Get Entry**: `GET /api/v1/entries/<id>/`
  - Returns: Single entry details
  - Status: ✅ **WORKING**

- **Update Entry**: `PUT /api/v1/entries/<id>/`
  - Accepts: metric_type, value, description
  - Returns: Updated entry
  - Status: ✅ **WORKING** (backend ready)

- **Delete Entry**: `DELETE /api/v1/entries/<id>/`
  - Returns: 204 No Content
  - Status: ✅ **WORKING**

#### Statistics API ✅
- **Get Stats**: `GET /api/v1/stats/`
  - Returns: 
    ```json
    {
      "total_entries": 10,
      "recent_entries": 5,
      "recent_activity": 3,
      "metric_breakdown": [
        {
          "metric_type": "carbon",
          "total_value": 25.5,
          "avg_value": 5.1,
          "count": 5
        },
        ...
      ]
    }
    ```
  - Status: ✅ **WORKING**

### Frontend (React) - **PARTIALLY FUNCTIONAL**

#### Authentication UI ✅
- **Login Page**: `/login`
  - Form: email, password
  - Calls: `POST /api/v1/login/`
  - Stores token in localStorage
  - Status: ✅ **WORKING**

- **Register Page**: `/register`
  - Form: username, email, password, password_confirm
  - Calls: `POST /api/v1/register/`
  - Stores token in localStorage
  - Status: ✅ **WORKING**

- **Logout**: 
  - Clears token from localStorage
  - Redirects to login
  - Status: ✅ **WORKING**

#### Dashboard UI ⚠️ **HAS ISSUES**
- **View Entries**: 
  - Displays list of entries
  - Shows: metric type, value, description, date
  - Status: ✅ **WORKING**

- **Add Entry**: 
  - Modal form with: metric_type, value, description
  - Calls: `POST /api/v1/entries/`
  - Refreshes list after creation
  - Status: ✅ **WORKING**

- **Delete Entry**: 
  - Delete button on each entry
  - Calls: `DELETE /api/v1/entries/<id>/`
  - Refreshes list after deletion
  - Status: ✅ **WORKING**

- **View Entry Details**: 
  - Click entry to see details modal
  - Shows: metric_type, value, description, created_at
  - Status: ✅ **WORKING**

- **Statistics Display**: ⚠️ **BROKEN**
  - Frontend expects: `stats.total_carbon`, `stats.total_water`, `stats.total_energy`
  - Backend returns: `total_entries`, `recent_entries`, `metric_breakdown` (array)
  - Status: ❌ **NOT WORKING** - Data mismatch

- **Update Entry**: ❌ **MISSING**
  - Backend supports it, but no UI
  - Status: ❌ **NOT IMPLEMENTED**

---

## ❌ What's Missing or Broken

### Critical Issues (Must Fix for MVP)

1. **Statistics Display Mismatch** ❌
   - **Problem**: Frontend expects different data structure than backend provides
   - **Location**: `climatiqq-frontend/src/components/Dashboard.js` lines 126, 131, 136
   - **Fix Needed**: Update Dashboard to parse `metric_breakdown` array and calculate totals by metric type
   - **Priority**: HIGH

2. **Update Entry UI** ❌
   - **Problem**: No way to edit existing entries
   - **Backend**: Already supports `PUT /api/v1/entries/<id>/`
   - **Fix Needed**: Add edit button/modal to Dashboard
   - **Priority**: MEDIUM (can work without it, but limits functionality)

### Nice-to-Have (Not Critical for MVP)

3. **Token Refresh** ⚠️
   - **Problem**: No endpoint to refresh expired tokens
   - **Current**: Users must re-login after 24 hours
   - **Priority**: LOW (acceptable for MVP)

4. **Error Handling** ⚠️
   - **Problem**: Basic error handling exists but could be better
   - **Priority**: LOW

5. **Loading States** ✅
   - **Status**: Already implemented
   - **Priority**: N/A

---

## 🔧 What Needs to Be Fixed

### Fix 1: Statistics Display

**Current Backend Response**:
```json
{
  "total_entries": 10,
  "recent_entries": 5,
  "recent_activity": 3,
  "metric_breakdown": [
    {"metric_type": "carbon", "total_value": 25.5, "avg_value": 5.1, "count": 5},
    {"metric_type": "water", "total_value": 100.0, "avg_value": 20.0, "count": 5},
    {"metric_type": "energy", "total_value": 50.0, "avg_value": 10.0, "count": 5}
  ]
}
```

**Current Frontend Expects**:
```javascript
stats.total_carbon  // ❌ Doesn't exist
stats.total_water   // ❌ Doesn't exist
stats.total_energy  // ❌ Doesn't exist
```

**Solution**: Update Dashboard.js to calculate totals from `metric_breakdown`:
```javascript
// Calculate totals from metric_breakdown
const calculateTotals = (metricBreakdown) => {
  const totals = {
    total_carbon: 0,
    total_water: 0,
    total_energy: 0,
    total_digital: 0
  };
  
  metricBreakdown?.forEach(metric => {
    if (metric.metric_type === 'carbon') totals.total_carbon = metric.total_value;
    if (metric.metric_type === 'water') totals.total_water = metric.total_value;
    if (metric.metric_type === 'energy') totals.total_energy = metric.total_value;
    if (metric.metric_type === 'digital') totals.total_digital = metric.total_value;
  });
  
  return totals;
};
```

### Fix 2: Add Update Entry Feature

**What's Needed**:
1. Add "Edit" button to entry cards
2. Create edit modal (similar to add modal)
3. Pre-fill form with existing entry data
4. Call `PUT /api/v1/entries/<id>/` on submit
5. Refresh list after update

---

## 📋 MVP Checklist

### Core Features
- [x] User registration
- [x] User login
- [x] JWT authentication
- [x] Create impact entries
- [x] List impact entries
- [x] View entry details
- [x] Delete entries
- [ ] Update entries (backend ready, frontend missing)
- [ ] View statistics (broken - data mismatch)

### Technical Requirements
- [x] Backend API fully functional
- [x] Frontend authentication working
- [x] Protected routes
- [x] Token storage (localStorage)
- [ ] Statistics display working
- [ ] Error handling (basic exists, could improve)

### Deployment Ready
- [x] Docker configuration
- [x] Database migrations
- [x] Environment variables
- [ ] Production settings (DEBUG=False, etc.)
- [ ] CORS properly configured for production

---

## 🚀 How to Get MVP Working

### Step 1: Fix Statistics Display (HIGH PRIORITY)

**File**: `climatiqq-frontend/src/components/Dashboard.js`

**Change lines 123-144** to parse `metric_breakdown`:

```javascript
// Add helper function at top of component
const getMetricTotal = (metricType) => {
  if (!stats.metric_breakdown) return 0;
  const metric = stats.metric_breakdown.find(m => m.metric_type === metricType);
  return metric ? metric.total_value : 0;
};

// Update stat cards:
<div className="stat-number">{getMetricTotal('carbon') || 0}</div>
<div className="stat-number">{getMetricTotal('water') || 0}</div>
<div className="stat-number">{getMetricTotal('energy') || 0}</div>
```

### Step 2: Add Update Entry Feature (MEDIUM PRIORITY)

1. Add edit state to Dashboard
2. Add "Edit" button to entry cards
3. Create edit modal
4. Implement update API call

### Step 3: Test Complete Flow

1. Register new user
2. Login
3. Create entries
4. View entries
5. View statistics (after fix)
6. Delete entry
7. Update entry (after implementation)

---

## 📊 Current MVP Status: **85% Complete**

### What Works ✅
- Full authentication flow
- CRUD operations (except Update UI)
- Basic dashboard
- Entry management

### What's Broken ❌
- Statistics display (data mismatch)

### What's Missing ⚠️
- Update entry UI
- Token refresh endpoint
- Enhanced error handling

---

## 🎯 Next Steps to Complete MVP

1. **Fix statistics display** (30 minutes)
   - Update Dashboard.js to parse metric_breakdown
   - Test with real data

2. **Add update entry feature** (1-2 hours)
   - Add edit modal
   - Wire up PUT request
   - Test update flow

3. **Test complete user journey** (30 minutes)
   - Register → Login → Create → View → Update → Delete → Stats

4. **Deploy to staging** (1 hour)
   - Configure production settings
   - Test in staging environment

---

## 📝 Summary

**The MVP is 85% complete!** 

The core functionality works:
- ✅ Users can register and login
- ✅ Users can create and view entries
- ✅ Users can delete entries
- ⚠️ Statistics display needs fixing (quick fix)
- ⚠️ Update feature needs UI (backend ready)

**Main blocker**: Statistics display mismatch between frontend expectations and backend response. This is a 30-minute fix.

**After fixes**: You'll have a fully functional MVP that users can actually use to track their environmental impact!
