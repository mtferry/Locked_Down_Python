#ifndef Py_LOCKDOWN_H
#define Py_LOCKDOWN_H
#ifdef __cplusplus
extern "C" {
#endif

int lockdown_is_enabled;
long long lockdown_pointer_multiplier, lockdown_pointer_offset;

static inline void INIT_LOCKDOWN()
{
	lockdown_is_enabled = 0;
}

#define LOCKDOWN_EXCEPTION_STRING "lockdown is enabled"
#define RAISE_EXCEPTION_IF_LOCKDOWN_IS_ENABLED if(lockdown_is_enabled) { return PyErr_Format(PyExc_RuntimeError, LOCKDOWN_EXCEPTION_STRING); }
#define RAISE_EXCEPTION_AND_RETURN_IF_LOCKDOWN_IS_ENABLED(r) if(lockdown_is_enabled) { PyErr_SetString(PyExc_RuntimeError, LOCKDOWN_EXCEPTION_STRING); return r; }
#define LOCKDOWN_SAFE_POINTER(p) (lockdown_is_enabled ? (void*)((lockdown_pointer_multiplier*(long long)p)+lockdown_pointer_offset) : p)

#ifdef __cplusplus
}
#endif
#endif /* !Py_LOCKDOWN_H */
