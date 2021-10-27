setup:
	rm -rf setup
	mkdir setup

	cp -r ansible/* setup
	cp secrets.json setup/secrets.json

	cd setup && ansible-playbook -i 192.168.168.152, --ask-pass --extra-vars "@secrets.json" provision.yml

deploy:
	rm -rf deployment
	mkdir deployment

	# Copy ansible playbook, python code and secrets
	cp -r ansible/* deployment
	cd python && cp -r * ../deployment/roles/provision/files/
	rm -rf deployment/roles/provision/files/tests
	rm -rf deployment/roles/provision/files/.gitkeep
	cp secrets.json deployment/secrets.json

	# Authenticate Onedrive and create refresh token session.pickle
	cp secrets.json deployment/roles/provision/files/energymeter/backup/secrets.json
	cd deployment/roles/provision/files/energymeter/backup && python3 setup_onedrive.py
	rm -rf deployment/roles/provision/files/energymeter/backup/setup_onedrive.py
	rm -rf deployment/roles/provision/files/energymeter/backup/secrets.json

	# Execute playbook
	cd deployment && ansible-playbook -i 192.168.168.152, --ask-pass --extra-vars "@secrets.json" deploy.yml

test:
	cd python && python3 -m unittest discover -v

