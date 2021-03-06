// Copyright (c) 2016 CEF Python. See the Authors and License files.

#pragma once

#include "common/cefpython_public_api.h"
#include "include/cef_context_menu_handler.h"


class ContextMenuHandler : public CefContextMenuHandler
{
public:
    ContextMenuHandler(){}
    virtual ~ContextMenuHandler(){}

    typedef cef_event_flags_t EventFlags;

    void OnBeforeContextMenu(CefRefPtr<CefBrowser> browser,
                             CefRefPtr<CefFrame> frame,
                             CefRefPtr<CefContextMenuParams> params,
                             CefRefPtr<CefMenuModel> model) override;

    bool OnContextMenuCommand(CefRefPtr<CefBrowser> browser,
                              CefRefPtr<CefFrame> frame,
                              CefRefPtr<CefContextMenuParams> params,
                              int command_id,
                              EventFlags event_flags) override;

    void OnContextMenuDismissed(CefRefPtr<CefBrowser> browser,
                                CefRefPtr<CefFrame> frame) override;

private:
    IMPLEMENT_REFCOUNTING(ContextMenuHandler);
};
