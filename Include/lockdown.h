#ifndef Py_LOCKDOWN_H
#define Py_LOCKDOWN_H
#ifdef __cplusplus
extern "C" {
#endif

int lockdown_is_enabled;

#define LOCKDOWN_EXCEPTION_STRING "lockdown is enabled"
#define RAISE_EXCEPTION_IF_LOCKDOWN_IS_ENABLED if(lockdown_is_enabled) { return PyErr_Format(PyExc_RuntimeError, LOCKDOWN_EXCEPTION_STRING); }

#ifdef __cplusplus
}
#endif
#endif /* !Py_LOCKDOWN_H */
