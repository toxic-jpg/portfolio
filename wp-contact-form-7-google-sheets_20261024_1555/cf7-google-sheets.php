<?php
/**
 * Plugin Name: CF7 to Google Sheets
 * Description: Send Contact Form 7 submissions directly to Google Sheets via Apps Script webhook
 * Version: 1.0.0
 * Author: Your Name
 * License: GPLv2+
 */

if (!defined('ABSPATH')) exit;

class CF7_Google_Sheets {
    private $webhook_url;
    private $field_map;

    public function __construct() {
        add_action('wpcf7_before_send_mail', [$this, 'handle_submission'], 10, 1);
        add_action('admin_menu', [$this, 'admin_menu']);
        add_action('admin_init', [$this, 'register_settings']);
    }

    public function handle_submission($contact_form) {
        $submission = WPCF7_Submission::get_instance();
        if (!$submission) return;

        $posted_data = $submission->get_posted_data();
        $form_id = $contact_form->id();

        $mapped = $this->map_fields($posted_data, $form_id);
        if (empty($mapped)) return;

        $this->send_to_sheets($mapped, $form_id);
    }

    private function map_fields($data, $form_id) {
        $map = get_option("cf7gs_map_{$form_id}", []);
        $result = ['_timestamp' => current_time('mysql'), '_form_id' => $form_id];
        foreach ($map as $cf7_field => $sheet_col) {
            if (isset($data[$cf7_field])) {
                $result[$sheet_col] = is_array($data[$cf7_field]) ? implode(', ', $data[$cf7_field]) : $data[$cf7_field];
            }
        }
        return $result;
    }

    private function send_to_sheets($data, $form_id) {
        $webhook = get_option("cf7gs_webhook_{$form_id}", '');
        if (!$webhook) return;

        $args = [
            'method' => 'POST',
            'timeout' => 10,
            'headers' => ['Content-Type' => 'application/json'],
            'body' => json_encode($data),
        ];
        wp_remote_post($webhook, $args);
    }

    public function admin_menu() {
        add_submenu_page('wpcf7', 'CF7 → Google Sheets', 'Google Sheets', 'manage_options', 'cf7-google-sheets', [$this, 'admin_page']);
    }

    public function register_settings() {
        register_setting('cf7gs_options', 'cf7gs_webhook_' . (isset($_GET['form_id']) ? intval($_GET['form_id']) : ''));
        register_setting('cf7gs_options', 'cf7gs_map_' . (isset($_GET['form_id']) ? intval($_GET['form_id']) : ''));
    }

    public function admin_page() {
        $forms = WPCF7_ContactForm::find();
        $form_id = isset($_GET['form_id']) ? intval($_GET['form_id']) : ($forms ? $forms[0]->id() : 0);
        $webhook = get_option("cf7gs_webhook_{$form_id}", '');
        $map = get_option("cf7gs_map_{$form_id}", []);
        ?>
        <div class="wrap">
            <h1>CF7 → Google Sheets</h1>
            <form method="post" action="options.php">
                <?php settings_fields('cf7gs_options'); ?>
                <table class="form-table">
                    <tr>
                        <th scope="row">Select Form</th>
                        <td>
                            <select name="form_id" onchange="this.form.submit()">
                                <?php foreach ($forms as $f): ?>
                                    <option value="<?= $f->id() ?>" <?= selected($form_id, $f->id()) ?>><?= esc_html($f->title()) ?></option>
                                <?php endforeach; ?>
                            </select>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">Apps Script Webhook URL</th>
                        <td><input type="url" name="cf7gs_webhook_<?= $form_id ?>" value="<?= esc_attr($webhook) ?>" class="regular-text" required></td>
                    </tr>
                </table>
                <h2>Field Mapping</h2>
                <p>Map CF7 field names (e.g. <code>your-name</code>, <code>your-email</code>) to Google Sheet column headers.</p>
                <table class="widefat" id="field-map-table">
                    <thead><tr><th>CF7 Field</th><th>Sheet Column</th><th></th></tr></thead>
                    <tbody>
                        <?php foreach ($map as $cf7 => $sheet): ?>
                            <tr>
                                <td><input type="text" name="cf7gs_map_<?= $form_id ?>[<?= esc_attr($cf7) ?>]" value="<?= esc_attr($cf7) ?>" class="small-text"></td>
                                <td><input type="text" name="cf7gs_map_<?= $form_id ?>[<?= esc_attr($cf7) ?>]" value="<?= esc_attr($sheet) ?>" class="small-text"></td>
                                <td><button type="button" class="button button-secondary remove-row">Remove</button></td>
                            </tr>
                        <?php endforeach; ?>
                        <tr class="template-row" style="display:none;">
                            <td><input type="text" name="cf7gs_map_<?= $form_id ?>[NEW_FIELD]" class="small-text" placeholder="your-field"></td>
                            <td><input type="text" name="cf7gs_map_<?= $form_id ?>[NEW_FIELD]" class="small-text" placeholder="Column Header"></td>
                            <td><button type="button" class="button button-secondary remove-row">Remove</button></td>
                        </tr>
                    </tbody>
                </table>
                <button type="button" class="button" id="add-row">Add Mapping</button>
                <?php submit_button(); ?>
            </form>
        </div>
        <script>
            document.getElementById('add-row').onclick = () => {
                const tbody = document.querySelector('#field-map-table tbody');
                const clone = document.querySelector('.template-row').cloneNode(true);
                clone.style.display = '';
                clone.classList.remove('template-row');
                clone.querySelectorAll('input').forEach(i => i.name = i.name.replace('NEW_FIELD', 'field_' + Date.now()));
                tbody.appendChild(clone);
            };
            document.addEventListener('click', e => {
                if (e.target.classList.contains('remove-row')) e.target.closest('tr').remove();
            });
        </script>
        <?php
    }
}

new CF7_Google_Sheets();