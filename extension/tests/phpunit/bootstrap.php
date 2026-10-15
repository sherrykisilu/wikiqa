<?php

declare( strict_types=1 );

namespace MediaWiki\Parser {
	class ParserOutput {
		public array $modules = [];
		public function addModules( string $module ): void {
			$this->modules[] = $module;
		}
	}

	class Parser {
		private ParserOutput $output;
		public array $hooks = [];
		public function __construct() {
			$this->output = new ParserOutput();
		}
		public function getOutput(): ParserOutput {
			return $this->output;
		}
		public function setFunctionHook( string $name, callable $callback ): void {
			$this->hooks[$name] = $callback;
		}
	}
}

namespace {
	require_once __DIR__ . '/../../includes/ChecklistRenderer.php';
	require_once __DIR__ . '/../../includes/Hooks.php';
}
