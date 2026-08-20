// Launches the bundled Python backend (PyInstaller sidecar) alongside the
// window, and kills it when the app exits. In `tauri dev`, run the backend
// manually instead (see gui/README.md) — no sidecar binary exists yet then.
use tauri::Manager;
use tauri_plugin_shell::process::CommandChild;
use tauri_plugin_shell::ShellExt;

struct BackendProcess(std::sync::Mutex<Option<CommandChild>>);

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .manage(BackendProcess(std::sync::Mutex::new(None)))
        .setup(|app| {
            if let Ok(sidecar) = app.shell().sidecar("winder-backend") {
                match sidecar.spawn() {
                    Ok((_rx, child)) => {
                        let state = app.state::<BackendProcess>();
                        *state.0.lock().unwrap() = Some(child);
                    }
                    Err(err) => {
                        eprintln!("Failed to start winder-backend sidecar: {err}");
                    }
                }
            }
            Ok(())
        })
        .on_window_event(|window, event| {
            if let tauri::WindowEvent::CloseRequested { .. } = event {
                let child = window.state::<BackendProcess>().0.lock().unwrap().take();
                if let Some(child) = child {
                    let _ = child.kill();
                }
            }
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
